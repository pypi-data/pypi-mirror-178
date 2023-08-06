import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


Item {
    property var endTimestamp
    property bool isPermanentAccess: false
    property bool isCurrentUserPro: false
    readonly property var contentWidth: content.width

    width: content.width
    height: content.height

    property var timeLeft: null
    property var timeLeftStr: {
        var hrs = Math.floor(timeLeft / 3600);
        var min = Math.floor((timeLeft - (hrs * 3600)) / 60);
        var sec = timeLeft - (hrs * 3600) - (min * 60);
        return hrs + ":" + min.toString().padStart(2, "0") + ":" + sec.toString().padStart(2, "0")
    }

    signal timeEnded()

    Timer {
        id: timer

        interval: 200
        repeat: true
        onTriggered: {
            if (endTimestamp < Date.now() / 1000) {
                stop()
                timeEnded()
            }
            timeLeft = Math.round(endTimestamp - Date.now() / 1000)
        }
    }

    onEndTimestampChanged: {
        timer.stop()
        if (Date.now() / 1000 < endTimestamp) {
            timeLeft = Math.round(endTimestamp - Date.now() / 1000)
            timer.start()
        } else {
            timeLeft = 0
        }
    }

    Row {
        id: content

        spacing: 4
        height: childrenRect.height

        DS3.Icon {
            source: !timeLeft && !isPermanentAccess
                ? "qrc:/resources/images/Athena/common_icons/HubAccessLocked.svg"
                : "qrc:/resources/images/Athena/common_icons/HubAccessUnlocked.svg"
            color: ui.ds3.figure.secondary
        }

        DS3.Text {
            text: isPermanentAccess ? tr.permanent_access : !timeLeft ? tr.no_pro_permissions : timeLeftStr
            style: ui.ds3.text.body.SBold
            color: ui.ds3.figure.secondary
        }
    }

    DS.MouseArea {
        visible: !isPermanentAccess

        onClicked: popup.visible = !popup.visible
    }

    DS.PermissionsPopup {
        id: popup

        onChoosen: (choice, duration) => {
            isCurrentUserPro
                ? app.hub_management_module.profi_hub_access_request(hub, choice)
                : app.facility_module.request_permission_for_facility(facility.id, duration)
        }

        Connections {
            target: app.facility_module

            onRequestPermissionForFacilityResult: (duration) => {
                if (!duration) return
                Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS/InfoPopup.qml",
                    {
                        "text": duration != "PERMANENT"
                            ? util.insert(tr.request_access_sent_desktop, [duration / 3600])
                            : tr.permanent_access_request_sent_desktop
                    }
                )
            }
        }
    }
}
