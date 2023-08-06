import QtQuick 2.13
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: companyImageUpload

//  Mini button alias to change its props like source or onClicked
    property alias buttonMiniControl: buttonMiniControl
//  The sheet action element to open/close it from outside
    property alias sheetAction: sheetAction
//  A function to determine what happens on upload switch checked
    property var uploadSwitchChecked: () => {}
//  A function to determine what happens on delete switch checked
    property var deleteSwitchChecked: () => {}
//  The image rectange inside companyImage. Primarely for source manipulations
    property alias imageRect: companyImage.imageRect
//  Size of the image
    property int size: 200

    property var imageData: null
    property string companyLogo: {
        !!appCompany ?
         (appCompany.data.company_logo.images.filter((image) => image.resolution == "300x300")[0] || {"url": ""}).url
         : "https://ajax-cdn-stage.s3.eu-west-3.amazonaws.com/imagesvc/public/app_a911/image_5ff5851d54cfce61173350bf/64x64/download.jpeg"
    }

    width: size
    height: size

    Connections {
        target: app

        onNewImageReady: {
            app.company_module.upload_company_logo(data["path"], "original")
        }
    }

    opacity: enabled ? 1 : 0.4

    DS3.CompanyImageBig {
        id: companyImage

        size: parent.size
        name: !!appCompany ? appCompany.mc_short_name || companyName : "CompanyName"
    }

    DS3.ButtonMini {
        id: buttonMiniControl

        anchors {
            right: parent.right
            bottom: parent.bottom
        }

        enabled: parent.enabled
        source: "qrc:/resources/images/Athena/common_icons/Upload-M.svg"

        DS3.SheetAction {
            id: sheetAction

            title: tr.change_image
            parent: buttonMiniControl

            DS3.SettingsSingleSelection {
                atomTitle.title: tr.change_image
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
