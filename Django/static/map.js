var data = {};

var lat = document.getElementById('id_latitude');
lat.disabled = true;
var lon = document.getElementById('id_longitude');
lon.disabled = true;
var button = document.getElementsByClassName("btn-success");
button.disabled = true;

ymaps.ready(init);

function init() {
    var myPlacemark,
        myMap = new ymaps.Map('map', {
            center: [55.753994, 37.622093],
            zoom: 9,
            controls: ['zoomControl', 'searchControl',]
        }, {
            searchControlProvider: 'yandex#search'
        });

    myMap.events.add('click', function (e) {
        var coords = e.get('coords');

        data['coords'] = coords;
        lat.value = data['coords'][0];
        lon.value = data['coords'][1];
        button.disabled = false;

        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
        }
        else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
            });
        }
        getAddress(coords);
    });

    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'поиск...'
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true
        });
    }

    function getAddress(coords) {
        myPlacemark.properties.set('iconCaption', 'поиск...');
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);

            data['address'] = firstGeoObject.getAddressLine();

            myPlacemark.properties
                .set({
                    iconCaption: [
                        firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
                        firstGeoObject.getThoroughfare() || firstGeoObject.getPremise()
                    ].filter(Boolean).join(', '),
                    balloonContent: firstGeoObject.getAddressLine()
                });
        });
    }
}

