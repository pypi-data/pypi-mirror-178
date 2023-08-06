import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups


Item {
    anchors.fill: parent

    ScrollView {
        id: scrollView
        clip: true
        width: parent.width - 20
        anchors {
            top: parent.top
            right: parent.right
            bottom: deleteButton.top
        }

        ScrollBar.vertical: Custom.ScrollBar {
            parent: scrollView
            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }

            policy: {
                if (scrollView.contentHeight > scrollView.height) {
                    return ScrollBar.AlwaysOn
                }
                return ScrollBar.AlwaysOff
            }
        }

        ColumnLayout {
            spacing: 10
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

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.UserImage {
                    id: userImage
                    width: 80
                    height: 80
                    fontSize: 28
                    imageSource: currentObject ? (Object.keys(currentObject.photos).length !== 0 ? currentObject.photos["64x64"] : "") : ""
                    userName: currentObject ? currentObject.data.name : ""
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
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
                    visible: companyAccess.RRU_ADJUST

                    Custom.Button {
                        width: parent.width
                        text: tr.edit
                        transparent: true
                        color: ui.colors.green1
                        anchors.centerIn: parent

                        onClicked: {
                            application.debug("company -> company info -> rru -> edit rru")
                            editMode = true
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.a911_pozivnoy
                    value: currentObject ? currentObject.data.name : ""
                    valueText.font.pixelSize: 18
                    valueText.rightPadding: 15
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.maximumLineCount: 1
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.a911_gbr_number
                    distance: 12
                    value: currentObject ? currentObject.data.code : ""
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
                Layout.minimumHeight: phoneText.height + 24
                Layout.maximumHeight: phoneText.height + 24

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    id: phoneText
                    width: parent.width
                    key: tr.phone
                    value: {
                        if (!currentObject || currentObject.data.phone_numbers.length == 0) return tr.a911_unknown
                        var phones = []
                        for(var i=0; i<currentObject.data.phone_numbers.length; i++) {
                            phones.push(currentObject.data.phone_numbers[i].number)
                        }
                        return phones.join("<br>")
                    }
                    distance: 12
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
                Layout.minimumHeight: locationItem.valueText.lineCount * 20 + 56
                Layout.maximumHeight: locationItem.valueText.lineCount * 20 + 56

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    id: locationItem
                    width: parent.width
                    key: tr.a911_location_adress
                    distance: 12
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.rightPadding: 15
                    value: currentObject ? currentObject.data.address_line : ""
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
//                Layout.minimumHeight: 80
//                Layout.maximumHeight: 80
//
//                Rectangle {
//                    height: 1
//                    width: parent.width
//                    anchors.bottom: parent.bottom
//                    color: ui.colors.white
//                    opacity: 0.1
//                }
//
//                Custom.TextFieldStatic {
//                    width: parent.width
//                    key: tr.a911_location_coordinates
//                    distance: 12
//                    value: currentObject ? currentObject.data.location.latitude + ", " + currentObject.data.location.longitude : ""
//                    anchors {
//                        top: parent.top
//                        topMargin: 12
//                        left: parent.left
//                    }
//                }
//            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.a911_car_number_gbr
                    distance: 12
                    value: {
                        return currentObject ? currentObject.data.vehicle.registration_number : ""
                    }
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
                Layout.minimumHeight: transportText.height + 24
                Layout.maximumHeight: transportText.height + 24

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    id: transportText
                    width: parent.width
                    key: tr.a911_transpotr
                    distance: 12
                    value: currentObject ? currentObject.data.vehicle.description : ""
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.rightPadding: 15
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                }
            }
        }
    }

    Rectangle {
        id: deleteButton
        color: "transparent"
        width: parent.width
        height: 72
        anchors.bottom: parent.bottom
        visible: {
            if (appUser.role == "CMS_ENGINEER") return false
            return companyAccess.RRU_ADJUST
        }

        Custom.Button {
            width: parent.width - 32
            text: tr.a911_delete_gbr
            color: ui.colors.dark4
            textButton.color: ui.colors.white
            transparent: false
            anchors.centerIn: parent

            visible: companyAccess.RRU_DELETE

            onClicked: {
                application.debug("company -> company info -> rru -> delete rru")

                if (!currentObject) return

                var settings = {}
                settings["id"] = currentObject.id

                function task() {
                    app.fast_response_team_module.delete_fast_response_team(settings)
                }

                Popups.confirmation_deletion_popup(task)
            }
        }
    }
}