import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings" as AdvancedSettings

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3Popups.PopupStep {
//  Selected device
    property var device
//  Selected color
    property var selectedColor

    width: 500

    title: tr.lightswitch_select_color
    sidePadding: 24

    DS3.Spacing {
        height: 24
    }

    Column {
        width: parent.width

        spacing: 1

        Repeater {
            id: colorsRepeater

            width: parent.width

            model: device.colors

            DS3.SettingsContainerItem {
                width: parent.width
                height: deviceImage.height

                isFirst: index == 0
                isLast: index == colorsRepeater.count - 1

                DS3.DeviceSelectionSingle {
                    id: deviceImage

                    property var available_colors: ({
                        "PANEL_COLOR_UNSPECIFIED": tr.color_white,
                        "PANEL_COLOR_WHITE": tr.color_white,
                        "PANEL_COLOR_BLACK": tr.color_black,
                        "PANEL_COLOR_FOG": tr.color_fog,
                        "PANEL_COLOR_GRAPHITE": tr.color_graphite,
                        "PANEL_COLOR_GREY": tr.color_grey,
                        "PANEL_COLOR_IVORY": tr.color_ivory,
                        "PANEL_COLOR_OLIVE": tr.color_olive,
                        "PANEL_COLOR_OYSTER": tr.color_oyster
                    })

                    width: parent.width

                    deviceType: device.obj_type
                    deviceColor: modelData
                    deviceSubtype: device.subtype
                    atomTitle.title: available_colors[modelData]
                    checked: selectedColor == modelData || (modelData == "PANEL_COLOR_WHITE" && selectedColor == "PANEL_COLOR_UNSPECIFIED")
                    color: ui.ds3.figure.transparent

                    clickedArea.onClicked: {
                        currentColor.deviceColor = modelData
                        currentColor.atomTitle.title = atomTitle.title
                        goBack()
                    }
                }
            }
        }
    }

    DS3.Spacing {
        height: 24
    }
}
