import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: uploadImageMediaPopup
    objectName: "uploadImageFacilityMediaPopup"
    width: 360
    height: 440
    closePolicy: Popup.CloseOnEscape
    modal: true
    focus: true
    anchors.centerIn: parent
    property var imagePath: ""
    property var imageId: ""
    property var imageName: ""

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }
    contentItem:  Rectangle {
        id: body
        clip: true
        color:  ui.colors.dark3
        radius: 8
        anchors.fill: parent
        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.a911_upload_photo

            closeArea.onClicked: {
                uploadImageMediaPopup.close()
            }
        }
        Connections {
            target: app.facility_media_module
            onUploadFacilityMediaImage : {
                imagePath = url_facility_media_image
                imageId = image_id_facility_media_image
                imageName = image_name
            }
        }
        Connections {
            target: app

            onActionSuccess: {
                uploadImageMediaPopup.close()
            }

            onActionFailed: addButton.enabled = true
        }
        Item {
            id: uploadPhotosButton
            width: 120
            height: 50
            Custom.Button {
               width: 112
               height: 40
               text: tr.open_document
               transparent: true
               anchors.centerIn: parent
               onClicked: fileDialogFacilityMediaImage.open()
            }
            anchors {
                top: parent.top
                topMargin: 99
                left: parent.left
                leftMargin: 24
            }
        }

        Custom.FontText {
            text: imageName
            width: 157
            height: 35
            wrapMode: Text.WordWrap
            anchors {
                left: body.left
                leftMargin: 165
                verticalCenter: uploadPhotosButton.verticalCenter
            }
            color: ui.colors.light3
            elide: Text.ElideRight
            textFormat: Text.PlainText
            maximumLineCount: 1
        }

        Rectangle {
            id: contentRect
            width: parent.width - 64
            height: 215
            color: "transparent"

            anchors {
                top: uploadPhotosButton.bottom
                horizontalCenter: parent.horizontalCenter
            }

            Custom.TextFieldEdit {
                id: fileNameInput

                width: parent.width

                key: tr.a911_file_name
                valueText.control.text: imageName
                valueText.control.maximumLength: 100
                distance: 12
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
                }
            }
            Connections {
                target: app.facility_media_module
                onUploadFacilityMediaImageError: {
                    if (result['error']) {
                        Popups.text_popup(tr.error, result['error']['message'])
                    }
                    if (result['4']) {
                        fileNameInput.valueText.valid = false
                        fileNameInput.valueText.error = result['4'].message
                    }
                }
            }
            Rectangle {
                id: category
                width: parent.width
                height: 80
                anchors {
                    top: fileNameInput.bottom
                    topMargin: 8
                }
                color: "transparent"
                Custom.FontText {
                    text: tr.a911_type
                    color: ui.colors.white
                    opacity: 0.5
                }
                Custom.ComboBox {
                    id: categoryFacilityMedia
                    property var userModel: [tr.a911_driving_directions, tr.a911_building_plans]
                    property var serverModel: ["ROAD_MAP", "FLOOR_PLAN"]
                    copyVisible: false
                    width: parent.width
                    model: userModel
                    currentIndex: {
                        if (rowLayout.currentTab.objectName != "floorPlansBtn") return 0
                        return 1
                    }
                    backgroundRectangle.color: ui.colors.dark1
                    anchors {
                        bottom: parent.bottom
                    }
                }
            }
        }
        Rectangle {
            width: 328
            height: 1
            color: ui.colors.dark3
            anchors {
                bottom: body.bottom
                bottomMargin: 80
                right: body.right
            }
        }
        Custom.Button {
            id: addButton
            width: 296
            height: 40
            transparent: false
            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: body.bottom
                bottomMargin: 24
            }
            text: tr.add
            enabledCustom: imagePath ? true : false
            enabled: false
            onClicked: {
                addButton.enabled = false
                var settings = {}

                settings["image_id"] = imageId
                settings["caption"] = fileNameInput.valueText.control.text ? fileNameInput.valueText.control.text : "default"
                settings["category"] = categoryFacilityMedia.serverModel[categoryFacilityMedia.currentIndex]

                app.facility_media_module.create_facility_media(settings)
            }
        }

        Custom.FileDialogImages {
            id: fileDialogFacilityMediaImage
            onAccepted: {
                if (fileDialogFacilityMediaImage.fileUrls.length === 1) {
                    app.facility_media_module.upload_facility_media(fileDialogFacilityMediaImage.fileUrl)
                }
                fileDialogFacilityMediaImage.close()
            }
        }
    }
    Connections {
        target: app.facility_media_module
        onUploadFacilityMediaImage: {
            addButton.enabled = true
        }
    }
}