var data = {};

function get_problems() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/problems/', false);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                data['placemarks'] = JSON.parse(xhr.responseText)['problems'];
            }
        }
    };
    xhr.send();
}

function like(id, n, index) {
    console.log('send ' + n + ' . ID: ' + id);
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/vote/?like=' + n + '&id=' + id, false);

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                console.log('OK!');
                placemarks[index]['rating'] += n;
                document.getElementById(placemarks[index]['id']).innerHTML = placemarks[index]['rating'];
                document.getElementById('like-' + placemarks[index]['id']).disabled = true;
                document.getElementById('dislike-' + placemarks[index]['id']).disabled = true;
            }
        }
    };
    xhr.send();
}

get_problems();
var placemarks = data['placemarks'];

var tag = {
    true: 'Решено',
    false: 'В ожидании'
};

var colors = {
    true: '#1CA800',
    false: '#7000E0'
};

ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map('map', {
            center: [55.751574, 37.573856],
            zoom: 12,
            controls: ['zoomControl']
        }, {
            searchControlProvider: 'yandex#search'
        }), clusterer = new ymaps.Clusterer({
            preset: 'islands#invertedVioletClusterIcons',
            groupByCoordinates: false,
            clusterDisableClickZoom: true,
            clusterHideIconOnBalloonOpen: false,
            geoObjectHideIconOnBalloonOpen: false,
            clusterIconLayout: 'default#pieChart',
            clusterIconPieChartRadius: 25,
            clusterIconPieChartCoreRadius: 10,
            clusterIconPieChartStrokeWidth: 3,
            clusterBalloonLeftColumnWidth: 100,
            clusterBalloonContentLayoutWidth: 350,
            clusterBalloonContentLayoutHeight: 300,
            hasBalloon: true
        }),
        getColor = function (index) {
            return colors[placemarks[index]['status']];
        },
        getRatingColor = function (index) {
            return '#444'
        },
        getImgStyle = function (index) {
            if (placemarks[index]['img']) {
                return '';
            }
            return 'display: none;';
        },
        geoObjects = [];

    for (var i = 0; i < placemarks.length; i++) {
        geoObjects[i] = new ymaps.Placemark(
            placemarks[i]['coords'],
            {
                balloonContentBody: '<div class="balloon">' +
                    '<div class="image" style="' + getImgStyle(i) + '"><img class="image" src="' + placemarks[i]['img'] +
                    '" height="130" style="margin-bottom: 10px"><br></div>' +
                    '' +
                    '<b>' + placemarks[i]['title'] + '</b><br>' +
                    placemarks[i]['description'] + '<br>' +
                    '<div class="columns">' +
                    '<b class="status" style="border: 2px solid ' + getColor(i) + '; color: ' +
                    getColor(i) + '">' + tag[placemarks[i]['status']] + '</b>' +
                    '<b class="status" id="' + placemarks[i]['id'] + '" style="margin-left: 10px; border: 2px solid ' + getRatingColor(i) + '; color: ' +
                    getRatingColor(i) + '">' + placemarks[i]['rating'] + '</b>' + '</div>' +
                    '' + '<br>' +
                    '<div class="footer">' +
                    '<button id="like-' + placemarks[i]['id'] +'" class="icon-like fa fa-thumbs-up" onclick="like(' + placemarks[i]['id'] + ',' + 1 + ',' + i + ')"></button>' +
                    '<button id="dislike-' + placemarks[i]['id'] +'" class="icon-dislike fa fa-thumbs-down" onclick="like(' + placemarks[i]['id'] + ',' + -1 + ',' + i + ')"></button>' +
                    '<button class="error">Ошибка</button>' +
                    '</div>',
                clusterCaption: '<b style="color: ' + getColor(i) + '">Метка №' + (i + 1) + '</b>',
            },
            {
                preset: 'islands#violetIcon',
                iconColor: getColor(i),
            }
        );
    }

    clusterer.add(geoObjects);
    myMap.geoObjects.add(clusterer);

    myMap.setBounds(clusterer.getBounds(), {
        checkZoomRange: true
    });
}
