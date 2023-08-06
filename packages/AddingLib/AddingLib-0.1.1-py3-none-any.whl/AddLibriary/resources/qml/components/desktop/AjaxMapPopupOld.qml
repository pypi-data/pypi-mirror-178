import QtQuick 2.0
import QtQuick.Controls 2.1
import QtLocation 5.8
import QtPositioning 5.8
import QtGraphicalEffects 1.12


AjaxPopup {
    id: popup
    width: application.width * 0.7
    height: application.height * 0.7

    property var information: null
    // {"location":{"lat":50.4939907,"lon":30.4680436,"acc":17.218,"speed":0.0,"time":1555501922}}

    Rectangle {
        id: mapBody
        anchors.fill: parent
        color: "#252525"
        clip: true

        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        Map {
            id: map
            anchors.fill: parent
            plugin: mapPlugin
            zoomLevel: 16.5
            center: QtPositioning.coordinate(information.location.lat + 0.0003, information.location.lon)
            activeMapType: supportedMapTypes[supportedMapTypes.length - 1]

            copyrightsVisible: false
            color: "#252525"

            MapCircle {
                center: QtPositioning.coordinate(information.location.lat, information.location.lon)
                radius: information.location.acc
                color: "#fe0000"
                opacity: 0.3
                border.width: 0
            }

            MapQuickItem {
                id: marker
                anchorPoint.x: markerIco.width/2
                anchorPoint.y: markerIco.height
                coordinate: QtPositioning.coordinate(information.location.lat, information.location.lon)
                sourceItem: Item {
                    Image {
                        id: markerIco
                        visible: true
                        source: "qrc:/resources/images/icons/marker.png"
                    }

                    Rectangle {
                        id: markerTable
                        width: 230
                        height: 110
                        radius: 15
                        color: "#252525"
                        opacity: 0.9
                        border.width: 2
                        border.color: "#fe0000"

                        anchors {
                            bottom: markerIco.top
                            bottomMargin: 30
                            horizontalCenter: markerIco.horizontalCenter
                        }

                        Text {
                            id: coordTable
                            color: ui.colors.light1
                            opacity: 0.9
                            text: information.location.lat + ",  " + information.location.lon
                            font.family: roboto.name
                            font.pixelSize: 14
                            font.bold: true

                            anchors {
                                horizontalCenter: parent.horizontalCenter
                                top: parent.top
                                topMargin: 10
                            }
                        }

                        Text {
                            id: accTable
                            color: ui.colors.light1
                            opacity: 0.9
                            text: tr.accuracy + ":  " + information.location.acc + " " + tr.alt_m
                            font.family: roboto.name
                            font.pixelSize: 14
                            font.bold: false

                            anchors {
                                left: parent.left
                                leftMargin: 20
                                top: coordTable.bottom
                                topMargin: 10
                            }
                        }

                        Text {
                            id: speedTable
                            color: ui.colors.light1
                            opacity: 0.9
                            text: tr.speed + ":  " + information.location.speed + " " + tr.ms
                            font.family: roboto.name
                            font.pixelSize: 14
                            font.bold: false

                            anchors {
                                left: parent.left
                                leftMargin: 20
                                top: accTable.bottom
                                topMargin: 3
                            }
                        }

                        Text {
                            id: dateTable
                            color: ui.colors.light1
                            opacity: 0.9
                            text: tr.date + ":  " + information.location.time
                            font.family: roboto.name
                            font.pixelSize: 14
                            font.bold: false

                            anchors {
                                left: parent.left
                                leftMargin: 20
                                top: speedTable.bottom
                                topMargin: 3
                            }
                        }
                    }
                }
            }
        }

        Plugin {
            id: mapPlugin
            name: "osm"
            PluginParameter {
                name: "osm.mapping.host"
                value: "http://a.tile.openstreetmap.org/"
            }
        }
    }
}
