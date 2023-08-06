import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.12
import QtQuick.Layouts 1.13

CommonPart {
    Rectangle {
        id: unblockButton

        width: 40
        height: 22

        anchors {
            top: parent.top
            topMargin: 24
            right: parent.right
            rightMargin: deviceDelegate.settingsVisible ? 60 : 16
        }

        radius: height/2
        color: "#f64347"
        opacity: enabled ? 1 : 0.6
        enabled: !!hub && !!device && hub.online && device.online

        visible: {
            if (!hub || !hub.current_user.device_edit_access) return false
            if (!device || device.blocked == "N/A" || device.blocked == "0") return false
            return true
        }

        Image {
            id: unblockImg

            width: 32
            height: 32

            anchors.centerIn: parent

            visible: false
            source: "qrc:/resources/images/desktop/icons/unlock_unblock_open_lock_castle-128.png"
            sourceSize.width: 32
            sourceSize.height: 32
        }

        ColorOverlay {
            anchors.fill: unblockImg

            source: unblockImg
            color: ui.colors.light1
        }

        MouseArea {
            anchors.fill: parent

            onClicked: {
                app.hub_management_module.device_command(device, 9)
            }
        }
    }
}