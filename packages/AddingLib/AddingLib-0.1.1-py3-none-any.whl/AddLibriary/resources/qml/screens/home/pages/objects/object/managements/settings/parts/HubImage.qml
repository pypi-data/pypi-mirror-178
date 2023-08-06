import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/images.js" as Images

Item {
    width: parent.width
    height: parent.height

    Connections {
        target: app

        onNewImageReady: {
            if (data.obj == "hub") {
                var settings = {}
                settings["url"] = data["path"]
                settings["hub_id"] = hub.hub_id
                app.hub_management_module.upload_hub_photo(settings)
            }
        }
    }

    Rectangle {
        id: hubImage

        property var isUploadAvailable: {
            if (!hub) return false
            if (!hub.online) return false
            if (!devEnable || !hub.current_user.common_params_access) return false
            if (hub.state == "ARMED" || hub.state == "NIGHT_MODE") return false
            return true
        }

        width: 120
        height: 120

        anchors.centerIn: parent

        color: ui.ds3.bg.low
        radius: height / 2
        layer.enabled: hub.small_image_link.endsWith("00000000_small.jpg") ? false : true
        layer.effect: OpacityMask { maskSource: circle }

        DS3.Image {
            id: image

            property var imageData: null

            onImageDataChanged: {
                if (imageData) {
                    app.process_image(imageData, "hub")
                }
            }

            width: 120
            height: 120

            anchors.centerIn: parent

            source: !!hub.small_image_link && !hub.small_image_link.endsWith("00000000_small.jpg") ? hub.small_image_link : ""
            asynchronous: true
        }

        Rectangle {
            id: circle

            anchors.fill: hubImage

            radius: parent.radius
            visible: false
        }
    }

    Image {
        anchors.centerIn: parent

        width: 120
        height: 120

        source: {
            var type = "21"
            if (hub.hub_type == "YAVIR") {
                type = "yavir_hub"
            } else if (hub.hub_type == "YAVIR_PLUS" || hub.hub_type == "HUB_FIBRA") {
                type = "fibra_hub"
            }
            return Images.get_image(type, "Large", hub.color)
        }
        visible: image.status != Image.Ready
    }

    DS3.ButtonMini {
        id: photoIco

        source: "qrc:/resources/images/desktop/icons/Photo-M.svg"
        visible: {
            if (!devEnable || !hub.current_user.advanced_params_access) return false
            return hub && hub.small_image_link && hub.small_image_link != "WRONG"
        }

        anchors {
            bottom: hubImage.bottom
            right: hubImage.right
        }

        DS3.SheetAction {
            id: sheetAction

            title: tr.change_image

            parent: photoIco

            DS3.SettingsSingleSelection {
                atomTitle.title: tr.change_image

                switchChecked: () => {
                    imageFileDialog.target = image
                    imageFileDialog.open()
                    sheetAction.close()
                }
            }

            DS3.SettingsSingleSelection {
                atomTitle {
                    title: tr.delete
                    titleColor: ui.ds3.figure.attention
                }
                switchChecked: () => {
                    var settings = {}
                    settings["hub_id"] = hub.hub_id
                    app.hub_management_module.delete_hub_photo(settings)
                    sheetAction.close()
                }
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