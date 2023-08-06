import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as Popups

Item {
    anchors.fill: parent

    property var addTeam: false

    ScrollView {
        id: staffEditScrollView
        width: parent.width - 20
        anchors {
            top: parent.top
            right: parent.right
            bottom: saveButton.top
        }

        ScrollBar.vertical: Custom.ScrollBar {
            parent: staffEditScrollView
            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }

            policy: {
                if (staffEditScrollView.contentHeight > staffEditScrollView.height) {
                    return ScrollBar.AlwaysOn
                }
                return ScrollBar.AlwaysOff
            }
        }

        ColumnLayout {
            spacing: 4
            width: parent.width
            anchors {
                top: parent.top
                right: parent.right
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 112
                Layout.maximumHeight: 112
                visible: !addTeam

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }
                Item {
                    width: 80
                    height: 80
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }

                    Rectangle {
                        id: backgroundDropArea
                        width: 80
                        height: 80
                        radius: height / 2
                        anchors.centerIn: parent

                        property var deletedImage: false

                        Custom.UserImage {
                            id: userImageEdit
                            anchors.fill: backgroundDropArea
                            fontSize: 28
                            imageSource: {
                                if (backgroundDropArea.deletedImage || addTeam) return ""
                                if (userImageEdit.urlRRUAvatar) return userImageEdit.urlRRUAvatar
                                if (Object.keys(currentObject.photos).length !== 0) return currentObject.photos["64x64"]
                                if (!userImageEdit.urlRRUAvatar || typeof currentObject.photos["64x64"] == "undefined") return ""
                            }
                            editing: true
                            userName: currentObject ? currentObject.data.name : ""
                            property var rruImageId: ""
                            property var urlRRUAvatar: ""

                            Connections {
                                target: app.fast_response_team_module
                                onUploadAvatarRRUSuccess: {
                                     userImageEdit.urlRRUAvatar = url_rru_avatar
                                     userImageEdit.rruImageId = image_id
                                }
                            }
                            MouseArea {
                                anchors.fill: userImageEdit
                                preventStealing: true
                                onClicked: {
                                    application.debug("company -> company info -> rru -> edit -> upload rru image")
                                    fileDialogRRUAvatar.open()
                                }
                            }
                        }
                    }
                    Item {
                        visible: userImageEdit.imageSource === ""
                        width: 32
                        height: 32
                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 4
                            right: parent.right
                            rightMargin: 4
                        }
                        Image {
                            sourceSize.width: 32
                            sourceSize.height: 32
                            source: "qrc:/resources/images/icons/a-plus-button.svg"
                            anchors.centerIn: parent
                        }
                    }

                    Custom.DeleteIcon {
                        id: deleteIcon
                        width: 32
                        height: 32
                        img.sourceSize.width: 32
                        img.sourceSize.height: 32
                        visible: userImageEdit.rruImageId || (!addTeam && !backgroundDropArea.deletedImage && (Object.keys(currentObject.photos).length !== 0))
                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 4
                            right: parent.right
                            rightMargin: 4
                        }

                        Custom.HandMouseArea {
                            anchors.fill: parent
                            preventStealing: true
                            onClicked: {
                                application.debug("company -> company info -> rru -> edit -> delete rru image")
                                userImageEdit.rruImageId = ""
                                backgroundDropArea.deletedImage = true
                            }
                        }
                    }

                    DropArea {
                        anchors.fill: backgroundDropArea
                        enabled: true
                        onEntered: {
                            backgroundDropArea.opacity = 0.7
                            backgroundDropArea.border.color = "skyblue"
                            backgroundDropArea.border.width = 3
                        }
                        onDropped: {
                            backgroundDropArea.border.color = "transparent"
                            backgroundDropArea.opacity = 1
                            if (drop.hasUrls && drop.urls.length === 1) {
                                backgroundDropArea.deletedImage = false
                                app.fast_response_team_module.upload_avatar_rru(currentObject, drop.urls[0])
                            } else {
                                 // TODO add popups
                                 // console.log('one file only')
                            }
                        }
                        onExited: {
                           backgroundDropArea.border.color = 'transparent'
                           backgroundDropArea.opacity = 1
                        }
                    }
                }

                Custom.FileDialogImages {
                    id: fileDialogRRUAvatar
                    onAccepted: {
                        if (fileDialogRRUAvatar.fileUrls.length === 1) {
                            app.fast_response_team_module.upload_avatar_rru(currentObject, fileDialogRRUAvatar.fileUrl)
                            backgroundDropArea.deletedImage = false
                        }
                        fileDialogRRUAvatar.close()
                    }
                }

                Item {
                    width: 150
                    height: 48
                    anchors {
                        top: parent.top
                        topMargin: 12
                        right: parent.right
                        rightMargin: 16
                    }

                    Custom.Button {
                        width: parent.width
                        text: tr.cancel
                        transparent: true
                        color: ui.colors.white
                        anchors.centerIn: parent

                        onClicked: {
                            application.debug("company -> company info -> rru -> edit -> cancel")
                            editMode = false
                        }
                    }
                }
            }

            Rectangle {
                id: topLevelInputs
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: topLevelInputs.defaultFieldHeight
                Layout.maximumHeight: topLevelInputs.defaultFieldHeight

                property var defaultFieldHeight: 92

                RowLayout {
                    spacing: 16
                    anchors.fill: parent

                    Rectangle {
                        color: "transparent"
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        Custom.TextFieldEdit {
                            id: nameField
                            width: parent.width - 16
                            key: tr.a911_pozivnoy + ui.required
                            value: currentObject ? currentObject.data.name : ""
                            valueText.control.maximumLength: 50
                            distance: 12
                            anchors {
                                top: parent.top
                                topMargin: 12
                                left: parent.left
                            }
                            valueText.onValidChanged: {
                                if (gbrNumberField.valueText.valid && nameField.valueText.valid) {
                                    topLevelInputs.Layout.minimumHeight = topLevelInputs.defaultFieldHeight
                                    topLevelInputs.Layout.maximumHeight = topLevelInputs.defaultFieldHeight
                                }
                            }

                            Connections {
                                target: app.fast_response_team_module
                                onSaveFastResponseTeamValidationErrors: {
                                    if (!addTeam && result["2"]) {
                                        nameField.valueText.valid = false
                                        nameField.valueText.error = result["2"].message
                                    }
                                    if (!addTeam && result["4"]) {
                                        topLevelInputs.Layout.minimumHeight = topLevelInputs.defaultFieldHeight + 16
                                        topLevelInputs.Layout.maximumHeight = topLevelInputs.defaultFieldHeight + 16
                                        nameField.valueText.valid = false
                                        nameField.valueText.error = result["4"].message
                                    }
                                }
                                onCreateFastResponseTeamValidationErrors: {
                                    if (addTeam && result["2"]) {
                                        nameField.valueText.valid = false
                                        nameField.valueText.error = result["2"].message
                                    }
                                    if (addTeam && result["4"]) {
                                        topLevelInputs.Layout.minimumHeight = topLevelInputs.defaultFieldHeight + 16
                                        topLevelInputs.Layout.maximumHeight = topLevelInputs.defaultFieldHeight + 16
                                        nameField.valueText.valid = false
                                        nameField.valueText.error = result["4"].message
                                    }
                                }
                            }
                        }
                    }

                    Rectangle {
                        color: "transparent"
                        Layout.fillWidth: true
                        Layout.fillHeight: true

                        Custom.TextFieldEdit {
                            id: gbrNumberField
                            width: parent.width - 16
                            key: tr.a911_gbr_number + ui.required
                            value: currentObject ? currentObject.data.code : ""
                            valueText.control.validator: RegExpValidator { regExp: /[0-9]+/ }
                            valueText.control.maximumLength: 10
                            distance: 12
                            anchors {
                                top: parent.top
                                topMargin: nameField.keyText.contentHeight - 4
                                left: parent.left
                            }
                            valueText.onValidChanged: {
                                if (nameField.valueText.valid && gbrNumberField.valueText.valid) {
                                    topLevelInputs.Layout.minimumHeight = 88
                                        topLevelInputs.Layout.maximumHeight = 88
                                }
                            }
                            Connections {
                                target: app.fast_response_team_module
                                onSaveFastResponseTeamValidationErrors: {
                                    if (!addTeam && result["3"]) {
                                        gbrNumberField.valueText.valid = false
                                        gbrNumberField.valueText.error = result["3"].message
                                    }
                                }
                                onCreateFastResponseTeamValidationErrors: {
                                    if (addTeam && result["3"]) {
                                        topLevelInputs.Layout.minimumHeight = 98
                                        topLevelInputs.Layout.maximumHeight = 98
                                        gbrNumberField.valueText.valid = false
                                        gbrNumberField.valueText.error = result["3"].message
                                    }
                                }
                            }
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: phoneEditField.height + 36
                Layout.maximumHeight: phoneEditField.height + 36

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.PhonesEdit {
                    id: phoneEditField
                    width: parent.width - 16
                    key: tr.phone
                    distance: 12
                    withType: false
                    maxPhoneNumbers: 2
                    emptyField: true
                    model: currentObject ? currentObject.data.phone_numbers : []
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    Connections {
                        target: app.fast_response_team_module
                        onSaveFastResponseTeamValidationErrors: {
                            if (!addTeam) phoneEditField.errorsResult(result)
                        }
                        onCreateFastResponseTeamValidationErrors: {
                            if (addTeam) phoneEditField.errorsResult(result)
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: addressField.height + 24
                Layout.maximumHeight: addressField.height + 24

                Custom.TextFieldEdit {
                    id: addressField
                    width: parent.width - 16
                    key: tr.a911_location_adress
                    value: currentObject ? currentObject.data.address_line : ""
//                    valueText.control.wrapMode: Text.WordWrap
                    valueText.control.maximumLength: 200
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                }
            }
//  Version ???
//            Rectangle {
//                color: "transparent"
//                Layout.fillWidth: true
//                Layout.minimumHeight: 88
//                Layout.maximumHeight: 88
//
//                Custom.TextFieldEdit {
//                    id: locationField
//                    width: parent.width - 16
//                    key: tr.a911_location_coordinates
//                    enabled: true
//                    valueText.control.maximumLength: 50
//                    value: {
//                        if (!currentObject) return ""
//                        return currentObject.data.location.latitude + ", "+ currentObject.data.location.longitude
//                    }
//                    distance: 12
//                    anchors {
//                        top: parent.top
//                        topMargin: 12
//                        left: parent.left
//                    }
//
//                    Custom.HandMouseArea {
//                        anchors.fill: parent
//                        onClicked: Popups.map_popup({"location":{"lat":50.4501,"lon":30.5234,"acc":17.218,"speed":0.0,"time":1555501922}}, "address")
//                    }
//                }
//            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 88
                Layout.maximumHeight: 88

                Custom.TextFieldEdit {
                    id: regNumberField
                    width: parent.width - 16
                    key: tr.a911_car_number_gbr
                    value: currentObject ? currentObject.data.vehicle.registration_number : ""
                    distance: 12
                    valueText.control.maximumLength: 10
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }

                    Connections {
                        target: app.fast_response_team_module
                        onSaveFastResponseTeamValidationErrors: {
                            if (!addTeam && result["8.1"]) {
                                gbrNumberField.valueText.valid = false
                                gbrNumberField.valueText.error = result["8.1"].message
                            }
                        }
                        onCreateFastResponseTeamValidationErrors: {
                            if (addTeam && result["8.1"]) {
                                gbrNumberField.valueText.valid = false
                                gbrNumberField.valueText.error = result["8.1"].message
                            }
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 88
                Layout.maximumHeight: 88

                Custom.TextFieldEdit {
                    id: descriptionField
                    width: parent.width - 16
                    key: tr.a911_transpotr
                    value: currentObject ? currentObject.data.vehicle.description : ""
                    distance: 12
                    valueText.control.maximumLength: 100
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
    }

    Rectangle {
        id: saveButton
        width: parent.width
        height: addTeam ? 88 : 72
        radius: addTeam ? 10 : 0
        color: addTeam ? ui.colors.dark3 : ui.colors.dark2
        anchors.bottom: parent.bottom

        Rectangle {
            width: parent.width - 21
            height: 1
            color: ui.colors.white
            opacity: 0.1
            visible: addTeam
            anchors.right: parent.right
        }

        Custom.Button {
            width: parent.width - 32
            text: {
                return addTeam ? tr.a911_add_crew : tr.a911_save_changes
            }
            transparent: false
            color: ui.colors.green1
            anchors.centerIn: parent
            enabledCustom: nameField.valueText.control.text.length > 0 && gbrNumberField.valueText.control.text.length > 0

            onClicked: {
                application.debug("company -> company info -> rru -> edit -> save")

                saveButton.forceActiveFocus()
                var phones = []
                phoneEditField.listView.model.forEach(function(phone) {
                    phones.push(phone)
                })

                var settings = {}
                settings["name"] = nameField.valueText.control.text
                settings["code"] = gbrNumberField.valueText.control.text
                settings["phone_numbers"] = phones
                settings["address_line"] = addressField.valueText.control.text
                settings["active"] = true
                settings["vehicle"] = {"registration_number": regNumberField.valueText.control.text, "description": descriptionField.valueText.control.text}
//                settings["location"] = util.get_coordinates(locationField.valueText.control.text)
                if (backgroundDropArea.deletedImage || addTeam) {
                   settings["logo_id"] = ""
                } else {
                    settings["logo_id"] = userImageEdit.rruImageId ? userImageEdit.rruImageId : currentObject.logo_id
                }

                if (!addTeam) {
                    app.fast_response_team_module.update_fast_response_team(currentObject, settings)
                } else {
                    app.fast_response_team_module.create_fast_response_team(settings)
                }
            }
        }
    }

    Component.onCompleted: {
        nameField.valueText.control.forceActiveFocus()
    }

    Connections {
        target: currentObject

        onActionSuccess: {
            if (!currentObject) return
            editMode = false
        }
    }
}