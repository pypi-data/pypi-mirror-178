import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


Item {
    width: parent.width
    height: footerItem.height

    DS3.MouseArea {
        cursorShape: Qt.ArrowCursor

        pressAndHoldInterval: 2500
        onPressAndHold: {
            var data = device.get_full_data()
            util.set_clipboard_text(data)
        }
    }

    DS3.InfoFooter {
        id: footerItem

        title.text: device.view_name
        subtitleUpper {
            text: `Device ID <a
                href="#" style="text-decoration:none; color:${
                    !!subtitleUpper.hoveredLink ? ui.ds3.figure.base : ui.ds3.figure.secondary
                }">
                    ${device.device_id.toUpperCase()}
                </a>`
            onLinkActivated: () => {
                util.set_clipboard_text(device.device_id)
                popupCopy.text = `${device.device_id} ${tr.copied}`
                popupCopy.open()
            }
        }
        subtitleLower {
            text: util.insert(tr.device_index_911, [device.device_index])
        }

        DS3Popups.PopupCopy {
            id: popupCopy
        }
    }
}
