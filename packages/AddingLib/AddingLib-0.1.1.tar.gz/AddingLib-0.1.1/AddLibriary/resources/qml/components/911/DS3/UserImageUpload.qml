import QtQuick 2.13
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {

//  Mini button alias to change its props like source or onClicked
    property alias buttonMiniControl: buttonMiniControl
//  The sheet action element to open/close it from outside
    property alias sheetAction: sheetAction
//  A function to determine what happens on upload switch checked
    property var uploadSwitchCheckedCallback: () => {}
//  A function to determine what happens on delete switch checked
    property var deleteSwitchCheckedCallback: () => {}
//  The image rectange inside the User Image Upload. Primarely for source manipulations
    property alias imageRect: userImage.imageRect
//  Size of the image
    property int size: 136

    width: size
    height: size

    Connections {
        target: app

        onNewImageReady: {
        //  A little hack to make QML think that the source has changed
        //  Otherwise it will not see the changes in the content
            userImage.imageRect.source = ""
            userImage.imageRect.source = data["path"]
        }
    }

    opacity: enabled ? 1 : 0.4

    DS3.UserImage {
        id: userImage
    }

    DS3.ButtonMini {
        id: buttonMiniControl

        anchors {
            right: parent.right
            bottom: parent.bottom
        }

        enabled: parent.enabled
        source: "qrc:/resources/images/Athena/notifications/Photo-M.svg"

        DS3.SheetAction {
            id: sheetAction

            title: tr.change_image
            parent: buttonMiniControl

            DS3.SettingsSingleSelection {
                atomTitle.title: tr.change_image
                switchChecked: uploadSwitchCheckedCallback
            }

            DS3.SettingsSingleSelection {
                atomTitle {
                    title: tr.delete
                    titleColor: ui.ds3.figure.attention
                }
                switchChecked: deleteSwitchCheckedCallback
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