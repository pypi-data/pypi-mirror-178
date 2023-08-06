import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/desktop/"


Rectangle {
    id: chimesSettings

    anchors.fill: parent

    color: ui.colors.dark1

    property var chimesItem: null

    Text {
        id: chimesTitle

        anchors {
            top: chimesSettings.top
            topMargin: 12
            horizontalCenter: parent.horizontalCenter
        }

        text: tr.chimes_title
        font.family: roboto.name
        font.pixelSize: 20
        font.weight: Font.Bold
        color: ui.colors.light1
    }

    Item {
        id: settingsContainer

        anchors {
            fill: parent
            top: chimesTitle.bottom
        }

        Item {
            id: plugItem

            anchors.fill: parent

            visible: !chimesItem.isMainSensorChecked && !chimesItem.isExternalContactChecked && !chimesItem.isBistable

            Image {
                id: plugImage

                width: 136
                height: 136

                anchors {
                    top: parent.top
                    topMargin: 104
                    horizontalCenter: parent.horizontalCenter
                }

                source: "qrc:/resources/images/desktop/chimes/ChimesPlug.svg"
            }

            Text {
                id: plugText

                anchors {
                    top: plugImage.bottom
                    topMargin: 24
                    horizontalCenter: parent.horizontalCenter
                }

                text: tr.no_endpoints_for_chimes
                width: parent.width - 40
                horizontalAlignment: Text.AlignHCenter
                font.family: roboto.name
                font.pixelSize: 14
                font.weight: Font.Light
                color: ui.colors.light1
                wrapMode: Text.WordWrap
            }
        }

        Item {
            id: advancedSettings

            anchors.fill: parent

            visible: !plugItem.visible

            Item {
                id: playChimesEachTime

                width: parent.width
                height: childrenRect.height

                anchors {
                    top: parent.top
                    topMargin: 30
                    horizontalCenter: parent.horizontalCenter
                }

                Text {
                    id: playChimesEachTimeTitle

                    anchors {
                        horizontalCenter: parent.horizontalCenter
                        top: parent.top
                        topMargin: 24
                    }

                    text: tr.play_chimes_each_time
                    font.family: roboto.name
                    font.pixelSize: 14
                    font.weight: Font.Light
                    color: ui.colors.light1
                    horizontalAlignment: Text.AlignHCenter
                }

                Column {
                    id: playChimesEachTimeSelection

                    width: parent.width - 32

                    anchors {
                        top: playChimesEachTimeTitle.bottom
                        topMargin: 12
                        horizontalCenter: parent.horizontalCenter
                    }

                    spacing: 2

                    Item {
                        id: ifOpeningDetected

                        width: parent.width
                        height: 40

                        visible: chimesItem.isMainSensorChecked

                        Text {
                            anchors {
                                left: parent.left
                                leftMargin: 12
                                verticalCenter: parent.verticalCenter
                            }

                            text: tr.if_opening_detected
                            font.family: roboto.name
                            font.pixelSize: 14
                            font.weight: Font.Light
                            color: ui.colors.light1
                        }

                        AjaxSwitch {
                            anchors.right: parent.right

                            checked: chimesItem.chimeTriggers.includes("CHIME_REED")

                            area.onClicked: {
                                var triggers = chimesItem.chimeTriggers
                                if (checked) {
                                    var index = triggers.indexOf("CHIME_REED");
                                    triggers.splice(index, 1)
                                    chimesItem.chimeTriggers = triggers
                                } else {
                                    chimesItem.chimeTriggers = triggers.concat(["CHIME_REED"])
                                }
                            }
                        }
                    }

                    Item {
                        id: ifExternalContactOpened

                        width: parent.width
                        height: 40

                        visible: chimesItem.isExternalContactChecked

                        Text {
                            anchors {
                                left: parent.left
                                leftMargin: 12
                                verticalCenter: parent.verticalCenter
                            }

                            text: ["1d", "11"].includes(device.obj_type) ? tr.if_device_triggered : tr.if_external_contact_opened
                            font.family: roboto.name
                            font.pixelSize: 14
                            font.weight: Font.Light
                            color: ui.colors.light1
                        }

                        AjaxSwitch {
                            anchors.right: parent.right

                            checked: {
                                if (device.obj_type === "1d") {
                                    return chimesItem.chimeTriggers.includes("CHIME_EXTRA_CONTACT_S2")
                                }
                                return chimesItem.chimeTriggers.includes("CHIME_EXTRA_CONTACT")
                            }

                            area.onClicked: {
                                var triggers = chimesItem.chimeTriggers

                                if (device.obj_type === "1d") {
                                    if (checked) {
                                        var index = triggers.indexOf("CHIME_EXTRA_CONTACT_S2");
                                        triggers.splice(index, 1)
                                        chimesItem.chimeTriggers = triggers
                                    } else {
                                        chimesItem.chimeTriggers = triggers.concat(["CHIME_EXTRA_CONTACT_S2"])
                                    }
                                }

                                else {
                                    if (checked) {
                                        var index = triggers.indexOf("CHIME_EXTRA_CONTACT");
                                        triggers.splice(index, 1)
                                        chimesItem.chimeTriggers = triggers
                                    } else {
                                        chimesItem.chimeTriggers = triggers.concat(["CHIME_EXTRA_CONTACT"])
                                    }
                                }
                            }
                        }
                    }

                    Text {
                        id: playChimesEachTimeSelectionInfo

                        width: parent.width - 44

                        anchors.horizontalCenter: parent.horizontalCenter

                        text: tr.chime_device_settings_info
                        horizontalAlignment: Text.AlignHCenter
                        color: ui.colors.middle1
                        font.family: roboto.name
                        font.pixelSize: 12
                        font.weight: Font.Light
                        wrapMode: Text.WordWrap
                    }
                }

                Text {
                    id: ringtoneTitle
                    anchors {
                        top: playChimesEachTimeSelection.bottom
                        topMargin: 36
                        horizontalCenter: parent.horizontalCenter
                    }
                    text: tr.sounds_title
                    font.family: roboto.name
                    font.pixelSize: 14
                    font.weight: Font.Light
                    color: ui.colors.light1
                }

                ListView {
                    id: ringtoneTitleSelection

                    width: parent.width - 32
                    height: 200

                    anchors {
                        top: ringtoneTitle.bottom
                        topMargin: 12
                        horizontalCenter: parent.horizontalCenter
                    }

                    interactive: false
                    model: [tr.one_beep, tr.two_beeps, tr.three_beeps, tr.four_beeps]

                    delegate: Item {
                        id: ringtoneTitleSelectionItem

                        width: parent.width
                        height: 40

                        Text {
                            anchors {
                                verticalCenter: parent.verticalCenter
                                left: parent.left
                                leftMargin: 12
                            }

                            text: modelData
                            font.family: roboto.name
                            font.pixelSize: 12
                            font.weight: Font.Light
                            color: ui.colors.light1
                        }

                        Image {
                            width: 24
                            height: 24

                            anchors {
                                verticalCenter: parent.verticalCenter
                                right: parent.right
                                rightMargin: 12
                            }

                            source: "qrc:/resources/images/desktop/chimes/ChimesSignalCheckMark.svg"

                            visible: chimesItem.chimeSignal == index
                        }

                        Rectangle {
                            width: parent.width
                            height: 1

                            color: ui.colors.middle4

                            anchors.bottom: parent.bottom
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor

                            onClicked: {
                                chimesItem.chimeSignal = index
                                app.chimes_module.play(index)
                            }
                        }
                    }
                }

                Rectangle {
                    id: importantBlock

                    width: parent.width - 48
                    height: childrenRect.height + 32

                    anchors {
                        horizontalCenter: parent.horizontalCenter
                        top: ringtoneTitleSelection.bottom
                    }

                    color: ui.colors.middle4
                    radius: 8

                    Text {
                        id: importantBlockTitle

                        anchors {
                            top: parent.top
                            left: parent.left
                            margins: 12
                        }

                        text: tr.chime_activation_settings
                        font.family: roboto.name
                        font.pixelSize: 16
                        font.weight: Font.Light
                        color: ui.colors.light1
                    }

                    Text {
                        id: importantBlockInfo

                        width: parent.width - 16

                        anchors {
                            top: importantBlockTitle.bottom
                            left: importantBlockTitle.left
                            topMargin: 8
                        }

                        text: tr.chime_activation_device_info
                        font.family: roboto.name
                        font.pixelSize: 14
                        font.weight: Font.Light
                        color: ui.colors.light1
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }
    }
}