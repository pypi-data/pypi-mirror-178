import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12
import QtWebEngine 1.8

import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/desktop/"


Rectangle {
    id: geofenceSettings

    property var sideMargin: 24
    property var lat: {
    return hub.geofence_latitude == "0.00000" ?
        "50.450001" :
        hub.geofence_latitude
    }
    property var lon: hub.geofence_longitude == "0.00000" ?
        "30.523333" :
        hub.geofence_longitude

    property var info: {"mode": "geofence", "info": {"lat": lat, "lon": lon, "radius": hub.geofence_radius || 15}}
    property var savePressed: false
    property var fullScreenPressed: false


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
            if (savePressed) {

                var settings = {
                    "geofence": {
                        "radius_meters": util.convert_distance_to_meters(circleRadius.value),
                        "coordinates": {
                            "latitude": {
                                "scale": 6,
                                "_decimal": info.info.lat,
                            },
                            "longitude": {
                                "scale": 6,
                                "_decimal": info.info.lon,
                            },
                        },
                    },
                    "_params": {
                        "skip_comparison_check": [
                            "geofence.coordinates.latitude.scale",
                            "geofence.coordinates.longitude.scale",
                        ],
                    },
                }
                DesktopPopups.please_wait_popup()
                app.hub_management_module.apply_update(management, hub, settings)
                savePressed = false
            }
            else if (fullScreenPressed) {
                DesktopPopups.popupByPath(
                    "qrc:/resources/qml/screens/home/pages/objects/object/popups/hub_settings/GeofenceMapPopup.qml",
                    {
                        "latitude": info.info.lat,
                        "longitude": info.info.lon,
                        "radius": info.info.radius,
                    }
                )
                fullScreenPressed = false
            }
        }
    }

    anchors.fill: parent

    color: ui.backgrounds.base

    DS3.NavBarModal {
        id: geofenceSettingsBar

        headerText: tr.geofence
        showCloseIcon: false
        isRound: false
        showManualIcon: true

        onManualAreaClicked: DesktopPopups.popupByPath(
            "qrc:/resources/qml/components/911/DS3/popups/ModalInfo.qml",
            {
                sections: [{
                    "description": tr.tap_and_hold_to_create_or_drag_n_drop_hub_location_pin
                }]
            }
        )
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: geofenceSettingsBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

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
            width: parent.width
            height: 436

            WebEngineView {
                id: webEngine

                width: 452
                height: 436

                anchors.horizontalCenter: parent.horizontalCenter
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
                        fullScreenPressed = true

                        webEngine.runJavaScript(
                            "get()",
                            function(result) { app.process_map_data(result) }  // get markers current coordinates
                        )
                    }
                }
            }
        }

        DS3.Spacing{
            height: 24
        }

        DS3.SettingsContainer {
            DS3.SettingsSliderValue {
                id: circleRadius

                width: parent.width

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

    DS3.ButtonBar {
        id: saveButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.save
        hasBackground: true
        enabled: devEnable && hub.current_user.advanced_params_access

        button.onClicked: {
            savePressed = true

            webEngine.runJavaScript(
                "get()",
                function(result) { app.process_map_data(result) }  // get markers current coordinates
            )
        }
    }
}