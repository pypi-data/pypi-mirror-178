import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3" as DS3

Item {
    width: parent.width
    height: 40

    property alias text: testText.text
    property alias icon: ethernetIcon.source

    opacity: enabled ? 1.0 : 0.4

    Item {
        width: 284
        height: 24

        anchors.centerIn: parent

        DS3.Image {
            id: ethernetIcon

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
            }

            width: 40
            height: 40

            source: "qrc:/resources/images/Athena/settings_icons/Ethernet-L.svg"
        }

        DS3.Text {
            id: testText

            anchors {
                verticalCenter: parent.verticalCenter
                left: ethernetIcon.right
                leftMargin: 12
            }

            color: ui.ds3.figure.interactive
            verticalAlignment: Text.AlignVCenter
            text: tr.ethernet_settings
            style: ui.ds3.text.body.MRegular

        }
        DS3.MouseArea {
            onClicked: {
                testLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/EthernetSettings.qml")
                popup.width = 722
            }
        }
    }
}