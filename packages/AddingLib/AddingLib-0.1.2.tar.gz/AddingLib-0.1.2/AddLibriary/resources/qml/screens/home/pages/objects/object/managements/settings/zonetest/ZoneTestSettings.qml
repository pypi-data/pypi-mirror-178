import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    property var sideMargin: 24

    anchors.fill: parent
    
    color: ui.ds3.bg.base
    
    DS3.NavBarModal {
        id: zoneTestSettingsBar

        headerText: tr.detection_zone_test
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: zoneTestSettingsBar.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.CommentImportant {
                atomTitle.title: tr.tap_on_devices_to_start_stop_detection_zone_test_multiple_selection_allowed
                visible: zoneTestSettings.visible
            }
        }

        DS3.Spacing {
            height: zoneTestSettings.visible ? 24 : 126
        }

        DS3.Image {
            sourceSize.width: 96
            sourceSize.height: 96

            anchors.horizontalCenter: parent.horizontalCenter

            source: "qrc:/resources/images/desktop/icons/ic-no-select-devices.svg"
            visible: !zoneTestSettings.visible
        }

        DS3.Spacing {
            height: zoneTestSettings.visible ? 0 : 16
        }

        DS3.Text {
            width: parent.width

            text: tr.you_have_no_connected_detectors_yet
            style: ui.ds3.text.body.LRegular
            visible: !zoneTestSettings.visible
            horizontalAlignment: Text.AlignHCenter
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            ListView {
                id: zoneTestSettings

                width: parent.width
                height: contentHeight

                spacing: 1
                model: management.filtered_devices_zone_test
                interactive: false
                visible: management.filtered_devices_zone_test.length
                section.property: "room_name"
                section.delegate:
                    Column {
                        width: parent.width

                        DS3.TitleSection {
                            width: parent.width

                            text: section
                        }

                        DS3.Spacing {
                            width: parent.width
                        }
                    }
                delegate: ZoneDeviceDelegate {}

            }
        }
    }
}


