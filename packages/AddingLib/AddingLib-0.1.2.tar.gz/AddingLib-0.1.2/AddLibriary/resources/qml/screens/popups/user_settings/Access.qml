import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3

Item {
    DS3.NavBarModal {
        id: navBarModal

        headerText: tr.a911_access
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        id: scrollView

        anchors {
            topMargin: navBarModal.height
        }

        width: parent.width

        contentSpacing: 24
        clip: true
        visible: appUser.multi_accepted_companies.length

        Repeater {
            model: appUser.multi_accepted_companies
            delegate: DS3.SettingsContainer {
                width: parent.width

                DS3.InfoImage {
                    width: parent.width

                    atomTitle.title: modelData.company_name
                    companyImage.source: modelData.company_logo.images.length === 0 ?
                        "" :
                        modelData.company_logo.images.filter((image) => image.resolution === "64x64").pop().url
                }

                Repeater {
                    model: modelData.role.roles
                    delegate: DS3.InfoTitle {
                        width: parent.width
                        height: 54

                        atomTitle.title: app.roles_to_ui([modelData])[0]

                        Connections {
                            target: tr

                            onTranslation_changed: atomTitle.title = app.roles_to_ui([modelData])[0]
                        }
                    }
                }
            }
        }
    }
}