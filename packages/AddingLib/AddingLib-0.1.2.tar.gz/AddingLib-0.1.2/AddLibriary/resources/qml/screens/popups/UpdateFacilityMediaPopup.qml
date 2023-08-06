import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"



AjaxPopup {
    id: updateImageMediaPopup
    objectName: "uploadImageFacilityMediaPopup"
    width: 360
    height: 368
    closePolicy: Popup.CloseOnEscape
    modal: true
    focus: true
    anchors.centerIn: parent

    property var media: null
    property var index: -1

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
            title: tr.a911_changing_file
            closeArea.onClicked: {
                updateImageMediaPopup.close()
            }
        }

        Rectangle {
            id: contentRect
            width: parent.width - 64
            height: 160
            color: "transparent"

            anchors {
                top: header.bottom
                horizontalCenter: parent.horizontalCenter
            }

            Custom.TextFieldEdit {
                id: fileNameInput

                width: parent.width

                key: tr.a911_file_name
                valueText.control.text: updateImageMediaPopup.media.caption
                distance: 12
                valueText.control.maximumLength: 100
                anchors {
                    top: parent.top
                    topMargin: 12
                    left: parent.left
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
                    currentIndex: serverModel.indexOf(media.category)

                    backgroundRectangle.color: ui.colors.dark1
                    anchors {
                        bottom: parent.bottom
                    }
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
        width: 296
        height: 40
        transparent: false
        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: body.bottom
            bottomMargin: 24
        }
        text: tr.save
        enabled: fileNameInput.valueText.control.text
        onClicked: {
            var settings = {}

            settings["id"] = media.id
            settings["category"] = categoryFacilityMedia.serverModel[categoryFacilityMedia.currentIndex]
            settings["caption"] = fileNameInput.valueText.control.text
            settings["image_id"] = media.image_id

            app.facility_media_module.update_facility_media(settings)
        }
        Connections {
            target: app
            onActionSuccess: {
                updateImageMediaPopup.close()
            }
        }
    }
}