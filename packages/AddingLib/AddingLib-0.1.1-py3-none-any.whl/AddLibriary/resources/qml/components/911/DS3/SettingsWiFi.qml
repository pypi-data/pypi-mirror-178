import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: settingsWiFi

//  Title of the settings
    property alias title: atomTitle.title
//  Wi-fi level
    property string wifiLevel: "NORMAL"
//  Choose locking
    property bool isLocked: false
//  On settings navigation clicked
    signal entered

    width: parent.width
    height: 54

    color: ui.ds3.bg.highest

    DS3.MouseArea {
        onClicked: parent.entered()
    }

    Item {
        id: wifiImageItem

        width: 40
        height: 16

        anchors {
            left: parent.left
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        DS3.Icon {
            anchors.left: parent.left

            source: "qrc:/resources/images/Athena/views_icons/UnlockFilled-S.svg"
            visible: !isLocked
        }

        DS3.Icon {
            anchors.left: parent.left

            source: "qrc:/resources/images/Athena/views_icons/LockFilled-S.svg"
            visible: isLocked
        }

        DS3.Image {
            id: wifiImage

            anchors.right: parent.right

            width: 16
            height: 16

            source: {
                var wifiImageMapper = {
                    "N/A": "qrc:/resources/images/Athena/common_icons/WiFi-0.svg",
                    "WEAK": "qrc:/resources/images/Athena/common_icons/WiFi-1.svg",
                    "NORMAL": "qrc:/resources/images/Athena/common_icons/WiFi-2.svg",
                    "STRONG": "qrc:/resources/images/Athena/common_icons/WiFi-3.svg"
                }

                if (Object.keys(wifiImageMapper).includes(wifiLevel)) {
                    return wifiImageMapper[wifiLevel]
                } else return wifiImageMapper["N/A"]
            }
        }
    }

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: wifiImageItem.right
            right: rightBlock.left
            margins: 16
            verticalCenter: parent.verticalCenter
        }
    }

    DS3.Icon {
        id: rightBlock

        anchors {
            right: parent.right
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/ChevronRight-S.svg"
        opacity: enabled ? 1 : 0.3
        visible: isLocked
    }
}