(function(window){
    function define_library() {
        var vanillaZoom = {};
        vanillaZoom.init = function(el) {

            var container = document.querySelector(el);
            if(!container) {
                console.error('No container element. Please make sure you are using the right markup.');
                return;
            }

            var firstSmallImage = container.querySelector('.small-preview');
            var zoomedImage = container.querySelector('.zoomed-image');

            if(!zoomedImage) {
                console.error('No zoomed image element. Please make sure you are using the right markup.');
                return;
            }

            if(!firstSmallImage) {
                console.error('No preview images on page. Please make sure you are using the right markup.');
                return;
            }
            else {
                zoomedImage.style.backgroundImage = 'url('+ firstSmallImage.src +')';
                firstSmallImage.classList.add('active');
            }   

            container.addEventListener("click", function (event) {
                var elem = event.target;

                if (elem.classList.contains("small-preview")) {
                    
                    var allSmallPreviews = container.querySelectorAll(".small-preview");
                    
                    allSmallPreviews.forEach(function (preview) {
                        preview.classList.remove('active');
                    })
                    
                    elem.classList.add('active');
                    
                    var imageSrc = elem.src;
                    zoomedImage.style.backgroundImage = 'url('+ imageSrc +')';
                }
            });
            
            zoomedImage.addEventListener('mouseenter', function(e) {
                this.style.backgroundSize = "250%"; 
            }, false);


            zoomedImage.addEventListener('mousemove', function(e) {
                
                var dimentions = this.getBoundingClientRect();

                var x = e.clientX - dimentions.left;
                var y = e.clientY - dimentions.top;

                var xpercent = Math.round(100 / (dimentions.width / x));
                var ypercent = Math.round(100 / (dimentions.height / y));

                this.style.backgroundPosition = xpercent+'% ' + ypercent+'%';
            
            }, false);


            zoomedImage.addEventListener('mouseleave', function(e) {
                this.style.backgroundSize = "contain"; 
                this.style.backgroundPosition = "left center"; 
            }, false);

        }
        return vanillaZoom;
    }

    if(typeof(vanillaZoom) === 'undefined') {
        window.vanillaZoom = define_library();
    }
    else{
        console.log("Library already defined.");
    }
})(window);