import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: timezoneEdit
    anchors.fill: parent
    color: ui.colors.dark3

    MouseArea {
        anchors.fill: parent
        onWheel: {}
    }

    property var currentTimezoneId: ""
    property var action: null

    RowLayout {
        spacing: 0
        anchors.fill: parent

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 7

            Rectangle {
                width: 64
                height: parent.height
                color: ui.colors.dark4
                anchors.left: parent.left

                Image {
                    sourceSize.width: 24
                    sourceSize.height: 24
                    source: "qrc:/resources/images/icons/back-arrow.svg"
                    anchors {
                        top: parent.top
                        topMargin: 24
                        horizontalCenter: parent.horizontalCenter
                    }
                }

                Custom.HandMouseArea {
                    onClicked: {
                        timezonesLoader.setSource("")
                    }
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 18

            Item {
                id: timezonesHeader
                width: parent.width
                height: !timezoneEdit.currentTimezoneId ? 124 : 184

                Rectangle {
                    width: parent.width
                    height: 1
                    color: ui.colors.white
                    opacity: 0.1
                    anchors.bottom: parent.bottom
                }

                RowLayout {
                    spacing: 0
                    anchors.fill: parent

                    Item {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        Layout.preferredWidth: 11

                        Item {
                            width: parent.width
                            height: parent.height - 48
                            anchors.bottom: parent.bottom

                            Custom.SearchField {
                                id: searchField
                                width: parent.width
                                height: 38
                                placeHolderText: tr.a911_search_via_timezone
                                anchors.top: parent.top

                                onSearchStarted: {
                                    timezones.filtered.set_filter(data)
                                }

                                Component.onCompleted: {
                                    if (timezoneEdit.currentTimezoneId) return

                                    searchField.control.text = timezones.find(timezones.current_timezone)
                                    searchField.control.forceActiveFocus(true)
                                }

                                Component.onDestruction: {
                                    timezones.filtered.set_filter("")
                                }
                            }

                            Rectangle {
                                width: parent.width
                                height: 40
                                radius: 10
                                color: ui.colors.dark1
                                visible: timezoneEdit.currentTimezoneId
                                anchors {
                                    top: searchField.bottom
                                    topMargin: 16
                                }

                                Custom.FontText {
                                    text: timezones.find(timezoneEdit.currentTimezoneId)
                                    color: ui.colors.light3
                                    font.pixelSize: 14
                                    width: parent.width - 80
                                    wrapMode: Text.WordWrap
                                    anchors {
                                        left: parent.left
                                        leftMargin: 24
                                        verticalCenter: parent.verticalCenter
                                    }
                                }

                                Image {
                                    sourceSize.width: 32
                                    sourceSize.height: 40
                                    source: "qrc:/resources/images/facilities/a-badge-green.svg"
                                    anchors {
                                        right: parent.right
                                        rightMargin: 16
                                        verticalCenter: parent.verticalCenter
                                    }
                                }

                                Custom.HandMouseArea {
                                    onClicked: {
                                        timezonesLoader.setSource("")
                                    }
                                }
                            }
                        }
                    }

                    Item {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        Layout.preferredWidth: 7
                    }
                }
            }

            Item {
                id: timezonesBody
                width: parent.width
                anchors {
                    top: timezonesHeader.bottom
                    bottom: parent.bottom
                    bottomMargin: 32
                }

                Item {
                    width: parent.width * 11 / 18
                    height: parent.height

                    Custom.EmptySpaceLogo {
                        size: parent.width / 2
                        visible: listView.model.length == 0
                    }
                }

                ListView {
                    id: listView
                    clip: true
                    spacing: 0
                    width: parent.width
                    boundsBehavior: Flickable.StopAtBounds
                    anchors {
                        top: parent.top
                        right: parent.right
                        bottom: parent.bottom
                    }

                    ScrollBar.vertical: Custom.ScrollBar {
                        id: control
                        parent: listView
                        policy: {
                            if (listView.contentHeight > listView.height) {
                                return ScrollBar.AlwaysOn
                            }
                            return ScrollBar.AlwaysOff
                        }
                        anchors {
                            top: parent.top
                            right: parent.right
                            bottom: parent.bottom
                        }
                    }

                    model: timezones.filtered

                    onContentHeightChanged: {
                        if (listView.contentHeight > listView.height) {
                            listView.footerPositioning = ListView.OverlayFooter
                        } else {
                            listView.footerPositioning = ListView.InlineFooter
                        }
                    }

                    footerPositioning: ListView.OverlayFooter
                    footer: Rectangle {
                        width: parent.width * 11 / 18
                        height: 8
                        clip: true
                        z: 1000
                        color: ui.colors.dark3

                        Rectangle {
                            width: parent.width + 6
                            height: 48
                            radius: 16
                            visible: listView.model.length > 0
                            color: ui.colors.dark4
                            anchors {
                                bottom: parent.bottom
                                horizontalCenter: parent.horizontalCenter
                            }
                        }
                    }

                    delegate: Rectangle {
                        width: parent.width * 11 / 18
                        height: 49
                        color: zoneArea.containsMouse ? ui.colors.dark2 : ui.colors.dark1

                        Rectangle {
                            width: parent.width
                            height: 1
                            color: zoneArea.containsMouse ? ui.colors.green3 : ui.colors.black
                            anchors.bottom: parent.bottom
                        }

                        Custom.FontText {
                            text: readable
                            color: ui.colors.light3
                            font.pixelSize: 14
                            width: parent.width - 80
                            wrapMode: Text.WordWrap
                            anchors {
                                left: parent.left
                                leftMargin: 24
                                verticalCenter: parent.verticalCenter
                            }
                        }

                        Image {
                            sourceSize.width: 32
                            sourceSize.height: 40
                            visible: zoneArea.containsMouse || zone.id == timezoneEdit.currentTimezoneId
                            source: zone.id == timezoneEdit.currentTimezoneId ? greenBadge : defaultBadge
                            anchors {
                                right: parent.right
                                rightMargin: 16
                                verticalCenter: parent.verticalCenter
                            }

                            property var greenBadge: "qrc:/resources/images/facilities/a-badge-green.svg"
                            property var defaultBadge: "qrc:/resources/images/facilities/a-badge-default.svg"
                        }

                        Custom.HandMouseArea {
                            id: zoneArea
                            hoverEnabled: true

                            onClicked: {
                                timezoneEdit.currentTimezoneId = zone.id
                                if (action) {
                                    action(timezoneEdit.currentTimezoneId)
                                }
                                timezonesLoader.setSource("")
                            }
                        }
                    }
                }
            }
        }
    }
}