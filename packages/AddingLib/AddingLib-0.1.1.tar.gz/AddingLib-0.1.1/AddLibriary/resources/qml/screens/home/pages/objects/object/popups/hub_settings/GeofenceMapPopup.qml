import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12
import QtWebEngine 1.8


import "qrc:/resources/qml/components/desktop/"

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
    id: popup

    width: application.width
    height: application.height

    header: Item {}
    footer: Item {}

    property var closePressed: false
    property var latitude: null
    property var longitude: null
    property var radius: null
    property var sideMargin: 24
    property var info: {"mode": "geofence", "info": {"lat": latitude, "lon": longitude, "radius": radius}}

    Connections {
        target: app

        onGeoData: {
            geofenceSettings.lat = data.latitude
            geofenceSettings.lon = data.longitude
            info = {
                "mode": "geofence",
                "info": {
                    "lat": data.latitude,
                    "lon": data.longitude,
                    "zoom": data.zoom,
                    "radius": util.convert_distance_to_meters(circleRadius.value),
                }
            }
            webEngine.loadHtml(app.get_map_html(info.info, info.mode))
            if (closePressed) {
                closePressed = false
                popup.close()
            }
        }
    }

    Component.onCompleted: {
        var information = {}
        information["lat"] = geofenceSettings.info.info.lat ? geofenceSettings.info.info.lat : "50.45466"
        information["lon"] = geofenceSettings.info.info.lon ? geofenceSettings.info.info.lon : "30.52380"
        information["zoom"] = data.zoom
        information["radius"] = util.convert_distance_to_meters(circleRadius.value)

        webEngine.runJavaScript(
            "get()",
            function(result) { app.process_map_data(result) }  // get markers current coordinates
        )

        var html = app.get_map_html(information, geofenceSettings.info.mode)
        webEngine.loadHtml(html)
    }

    Item {
        id: container

        width: application.width
        height: maxPopupHeight

        anchors {
            horizontalCenter: parent.horizontalCenter
        }

        WebEngineView {
            id: webEngine

            width: application.width
            height: application.height

            anchors {
                horizontalCenter: parent.horizontalCenter
            }
        }

        Rectangle {
            id: overButton

            height: 40
            width: 40

            anchors{
                top: parent.top
                topMargin: 10
                right: parent.right
                rightMargin: 10
            }

            color: "transparent"

            MouseArea {
                anchors.fill: parent

                onClicked: {
                    closePressed = true
                    webEngine.runJavaScript(
                        "get()",
                        function(result) { app.process_map_data(result) }  // get markers current coordinates
                    )
                }
            }
        }

        DS3.SettingsContainer {

            width: 452

            anchors {
                bottom: parent.bottom
                left: parent.left
                leftMargin: 24
            }

            DS3.SettingsSliderValue {
                id: circleRadius

                enabled: devEnable && hub.current_user.advanced_params_access
                title: tr.geofence_boundary
                value: settings.measure_system == "imperial" ?
                    Math.round(info.info.radius * 3.28 / 50) * 50 :
                    info.info.radius
                from: settings.measure_system == "imperial" ? 50 : 15
                to: settings.measure_system == "imperial" ? 9850 : 3000
                stepSize: settings.measure_system == "imperial" ? 50 : 15
                suffix: settings.measure_system == "imperial" ? tr.feet : tr.m

                onPressedChanged: {
                    if (!pressed) {
                        webEngine.runJavaScript(
                            "get()",
                            function(result) { app.process_map_data(result) }  // get markers current coordinates
                        )
                    }
                }
            }
        }
    }
}