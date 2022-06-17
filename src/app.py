import re
import threading
from datetime import datetime

import serial
from flask import Flask, render_template, request, jsonify, session, redirect

from parking_status import ParkingStatus
from user import User
from car import Car
from sensor import Sensor
from card import Card
from invoice import Invoice
from database_manager import DatabaseManager
import random

app = Flask(__name__, template_folder="../templates", static_folder="../assets")
app.secret_key = b'_5#y2L"FgTK9T30293124Q8z\n\126P5HL4YK7x\\ec]/'

database_manager = DatabaseManager()


def sensor_checker(database):
    arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)
    while arduino.is_open:
        while arduino.in_waiting:
            sensor_id = int.from_bytes(arduino.read(1), "big") + 1
            sensor_status = int.from_bytes(arduino.read(1), "big")

            print(sensor_id, sensor_status)

            sensor = database.get(Sensor, Sensor.id == sensor_id)
            if sensor is not None:
                sensor.parking_status = ParkingStatus(sensor_status)
                sensor.updated_at = datetime.now()
                database.save(sensor)

    print("Thread died")


threading.Thread(target=lambda: sensor_checker(database_manager)).start()


@app.route("/", methods=["GET"])
@app.route("/login", methods=["POST"])
def index():
    if "name" in session:
        return redirect("/dashboard")
    if request.method == "GET":
        return render_template("page.html")
    elif request.method == "POST":
        if "phone" in request.form:
            phone = request.form["phone"]

            if not phone.isdigit():
                return jsonify({"status": "error", "message": "Phone number must be digits"}), 400

            if len(phone) != 8:
                return jsonify({"status": "error", "message": "Phone number must be 8 digits"}), 400

            session["phone"] = phone

            user = database_manager.get(User, User.phone_number == phone)
            if user is None:
                return jsonify({"status": "register"}), 201
            else:
                code_a = random.randint(0, 9)
                code_b = random.randint(0, 9)
                code_c = random.randint(0, 9)
                code_d = random.randint(0, 9)

                print(code_a, code_b, code_c, code_d)

                session["code"] = str(code_a) + str(code_b) + str(code_c) + str(code_d)
                return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 400  # 400 means a bad request


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("page.html", other_page="components/register.html")
    elif request.method == "POST":
        if "name" in request.form and "phone" in request.form and "address" in request.form and "email" in request.form:
            name = request.form["name"]
            address = request.form["address"]
            email = request.form["email"]
            phone_number = request.form["phone"]

            if not len(name) > 0:
                return jsonify({"status": "error", "message": "Name cannot be empty"}), 400

            for char in name:
                if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ":
                    return jsonify({"status": "error", "message": "Name can only use letters A to Z"}), 400

            if not len(address) > 0:
                return jsonify({"status": "error", "message": "Address cannot be empty"}), 400

            pattern = re.compile("^[A-Za-z\d._+%-]+@[A-Za-z\d.-]+[.][A-Za-z]+$")
            if not pattern.match(email):
                return jsonify({"status": "error", "message": "Email is not valid"}), 400

            if not len(phone_number) > 0:
                return jsonify({"status": "error", "message": "Phone number cannot be empty"}), 400

            if not phone_number.isdigit():
                return jsonify({"status": "error", "message": "Phone number must be digits"}), 400

            if len(phone_number) != 8:
                return jsonify({"status": "error", "message": "Phone number must be 8 digits"}), 400

            user = User(name=name, address=address, email=email, phone_number=phone_number)

            if database_manager.save(user):
                session["name"] = name
                session["address"] = address
                session["email"] = email
                session["phone"] = phone_number
                return redirect("/")
            else:
                return redirect("/register")
        else:
            return redirect("/register")


@app.route("/login/confirm", methods=["GET", "POST"])
def confirm():
    if request.method == "GET":
        return render_template("page.html", other_page="components/confirm.html")
    elif request.method == "POST":
        if "codeA" in request.form and "codeB" in request.form and "codeC" in request.form and "codeD" in request.form:
            code_a = request.form["codeA"]
            code_b = request.form["codeB"]
            code_c = request.form["codeC"]
            code_d = request.form["codeD"]

            if code_a.isdigit() and code_b.isdigit() and code_c.isdigit() and code_d.isdigit():
                if session["code"] == code_a + code_b + code_c + code_d:
                    user = database_manager.get(User, User.phone_number == session["phone"])
                    if user is not None:
                        session["name"] = user.name
                        session["address"] = user.address
                        session["email"] = user.email
                        return redirect("/")
                    else:
                        return redirect("/login")
                else:
                    return jsonify({"status": "error", "message": "Code is incorrect"}), 400
            else:
                return jsonify({"status": "error", "message": "Code must be digits"}), 400
        else:
            return jsonify({"status": "error", "message": "Code is incorrect"}), 400


@app.route("/register/car", methods=["GET", "POST"])
def register_car():
    if "name" not in session:
        return redirect("/")

    if request.method == "GET":
        return render_template("page.html", other_page="components/register-car.html")
    elif request.method == "POST":
        if "license" in request.form:
            car_license = request.form["license"]

            car = database_manager.get(Car, Car.license_plate == car_license)
            if car is None:
                user = database_manager.get(User, User.phone_number == session["phone"])
                if user is not None:
                    car = Car(license_plate=car_license, owner=user.id)
                    if database_manager.save(car):
                        return jsonify({"status": "success"}), 200
                    else:
                        return jsonify({"status": "error", "message": "Could not save car"}), 400
            else:
                return jsonify({"status": "error"}), 400
        else:
            return jsonify({"status": "error"}), 400


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/users")
def users_route():
    return render_template("page.html", other_page="components/admin/users.html")


@app.route("/parking-history")
def parking_history_route():
    return render_template("page.html", other_page="components/user/parking-history.html")


@app.route("/user-profile", methods=["GET", "POST"])
def user_profile_route():
    if "name" not in session:
        return redirect("/")

    if request.method == "GET":
        return render_template('page.html', other_page="components/user/user-profile.html")
    elif request.method == "POST":
        user = database_manager.get(User, User.phone_number == session["phone"])
        if user is not None:
            session["name"] = user.name
            session["address"] = user.address
            session["email"] = user.email
            return redirect("/")


@app.route("/user-payment")
def user_payment_route():
    return render_template("page.html", other_page="components/user/user-payment.html")


@app.route("/user-parking-lot")
def user_parking_route():
    return render_template("page.html", other_page="components/user/user-parking-lot.html")


@app.route("/dashboard")
def dashboard():
    return render_template("page.html", other_page="components/admin/dashboard.html")


@app.route("/admin")
@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin.html", other_page="components/admin/dashboard.html")


@app.route("/map")
def parking_lot_map():
    sensors = database_manager.get_all(Sensor)
    json_sensors = []
    for sensor in sensors:
        json_sensors.append(sensor.serialize())
    return render_template("map.html", sensors=json_sensors)


@app.route("/test")
def test():
    users = database_manager.get_all(User)
    return render_template("test.html", users=users)


app.run(use_reloader=False)
