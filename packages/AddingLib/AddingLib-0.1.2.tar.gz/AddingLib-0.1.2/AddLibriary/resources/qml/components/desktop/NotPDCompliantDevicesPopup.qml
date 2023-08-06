import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.Popup {
    id: notPDComliantDevicesPopup

    property var not_pd_devices: null

    width: 400

    title: tr.some_devices_not_PD_certified
    hasCrossButton: false

    Repeater {
        id: repeater

        width: parent.width - 48

        model: not_pd_devices

        Item {
            width: repeater.width
            height: textBodyField.height

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.Text {
                id: textBodyField

                width: parent.width

                text: util.insert(tr.alt_in_alt, [modelData.name, modelData.room_name])
                style: ui.ds3.text.body.MRegular
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }

    DS3.Spacing {
        height: 8
    }

    DS3.Text {
        width: parent.width

        text: tr.devices_not_PD_certified_tip
        style: ui.ds3.text.body.MRegular
        horizontalAlignment: Text.AlignHCenter
    }

    DS3.Spacing {
        height: 48
    }

    DS3.ButtonContained {
        width: parent.width

        text: tr.ok

        onClicked: {
            notPDComliantDevicesPopup.close()
        }
    }
}
