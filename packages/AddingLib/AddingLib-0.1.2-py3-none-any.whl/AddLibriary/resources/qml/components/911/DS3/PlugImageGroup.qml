import QtQuick 2.13
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: groupImageRect

//  Mini button alias to change its props like source or onClicked
    property alias buttonMiniControl: buttonMiniControl
//  The sheet action element to open/close it from outside
    property alias sheetAction: sheetAction
//  A function to determine what happens on upload switch checked
    property var uploadSwitchChecked: () => {}
//  A function to determine what happens on delete switch checked
    property var deleteSwitchChecked: () => {}
//  The image rectange inside the Plug Image Group. Primarely for source manipulations
    property alias imageRect: groupImage.imageRect
//  Size of the image
    property int size: 136

    width: size
    height: size

    Connections {
        target: app

        onNewImageReady: {
        //  A little hack to make QML think that the source has changed
        //  Otherwise it will not see the changes in the content
            groupImage.imageRect.source = ""
            groupImage.imageRect.source = data["path"]
        }
    }

    Connections {
        target: app.hub_management_module

        onAddGroupSuccess: {
            if (groupImage.imageRect.imageData) {
                let settings = {
                    "url" : groupImage.imageRect.source.toString(),
                    "hub_id" : hub.hub_id,
                    "group_id" : group.group_id
                }

                app.hub_management_module.upload_group_photo(settings)
            }
        }
    }

    opacity: enabled ? 1 : 0.4

    DS3.GroupImage {
        id: groupImage

        size: 128
    }

    DS3.ButtonMini {
        id: buttonMiniControl

        anchors {
            right: parent.right
            bottom: parent.bottom
        }

        enabled: parent.enabled
        source: "qrc:/resources/images/Athena/views_icons/Photo-S.svg"

        DS3.SheetAction {
            id: sheetAction

            title: tr.change_image
            parent: buttonMiniControl

            DS3.SettingsSingleSelection {
                atomTitle.title: tr.a911_upload_photo
                switchChecked: uploadSwitchChecked
            }

            DS3.SettingsSingleSelection {
                atomTitle {
                    title: tr.delete
                    titleColor: ui.ds3.figure.attention
                }
                switchChecked: deleteSwitchChecked
            }
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            onClicked: {
                sheetAction.open()
            }
        }
    }
}
