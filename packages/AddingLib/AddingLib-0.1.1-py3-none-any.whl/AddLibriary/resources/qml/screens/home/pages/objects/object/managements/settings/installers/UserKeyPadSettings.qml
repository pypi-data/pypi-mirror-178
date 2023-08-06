import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    property var user: null
    property var sideMargin: 24

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: usersSettingsBar

        headerText: tr.user_password
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/UserSettings.qml", {'user': user})
        }
    }

    DS3.ScrollView {
        padding: sideMargin

        anchors {
            fill: undefined
            top: usersSettingsBar.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        DS3.InfoContainer {
            imageType: DS3.InfoContainer.ImageType.DeviceImage
            imageSource: Images.get_image("0a", "Medium", "BLACK")
            titleComponent.text: tr.user_password_settings
            descComponent.text: tr.user_password_description
        }

        DS3.Spacing {
            height: 28
        }

        DS3.TitleSection {
            text: tr.passcodes_plural
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
        }

        DS3.SettingsContainer {
            id: settingsContainer

            DS3.SettingsNavigationTitlePrimary {
                title: tr.user_password

                onEntered: DesktopPopups.popupByPath(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/ChangeUserKeyPadPassword.qml",
                    {"force": false, "user": user}
                )
            }

            DS3.SettingsNavigationTitlePrimary {
                title: tr.duress_code

                onEntered: DesktopPopups.popupByPath(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/ChangeUserKeyPadPassword.qml",
                    {"force": true, "user": user}
                )
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            DS3.CommentPasscode {
                atomTitle.title: tr.to_arm_the_system
                firstSubtitle.text: user.index.substring(user.index.length-2, user.index.length)
                firstIcon {
                    source: "qrc:/resources/images/Athena/common_icons/Asterisk-S.svg"
                    color: ui.ds3.figure.base
                }
                secondSubtitle.text: tr.user_password
                secondIcon {
                    source: "qrc:/resources/images/Athena/common_icons/Armed-S.svg"
                    color: ui.ds3.figure.base
                }
                thirdSubtitle.text: tr.button_user_code
            }

            DS3.CommentPasscode {
                atomTitle.title: tr.to_disarm_the_system
                firstSubtitle.text: user.index.substring(user.index.length-2, user.index.length)
                firstIcon {
                    source: "qrc:/resources/images/Athena/common_icons/Asterisk-S.svg"
                    color: ui.ds3.figure.base
                }
                secondSubtitle.text: tr.user_password
                secondIcon {
                    source: "qrc:/resources/images/Athena/common_icons/Disarmed-S.svg"
                    color: ui.ds3.figure.base
                }
                thirdSubtitle.text: tr.button_user_code
            }

            DS3.CommentPasscode {
                atomTitle.title: tr.if_you_are_in_danger
                firstSubtitle.text: user.index.substring(user.index.length-2, user.index.length)
                firstIcon {
                    source: "qrc:/resources/images/Athena/common_icons/Asterisk-S.svg"
                    color: ui.ds3.figure.base
                }
                secondSubtitle.text: tr.duress_code
                secondIcon {
                    source: "qrc:/resources/images/Athena/common_icons/Disarmed-S.svg"
                    color: ui.ds3.figure.base
                }
                thirdSubtitle.text: tr.button_user_code
            }
        }
    }
}