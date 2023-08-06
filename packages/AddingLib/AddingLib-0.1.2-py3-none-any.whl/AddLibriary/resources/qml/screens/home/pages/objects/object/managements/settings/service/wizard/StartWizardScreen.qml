import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/parts" as Parts


Rectangle {
    id: startWizardScreen

    property var sideMargin: 24

    color: ui.ds3.bg.base

    DS3.MouseArea {
        cursorShape: Qt.ArrowCursor
    }

    DS3.NavBarModal {
        id: startWizarBar

        headerText: tr.PD_compliance_wizard
        isRound: false
        showCloseIcon: false
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: startWizarBar.bottom
            bottom: nextButton.top
            left: parent.left
            right: parent.right
        }

        width: parent.width
        height: startWizardScreen.height

        padding: sideMargin

        DS3.InfoContainer {
            anchors.horizontalCenter: parent.horizontalCenter

            imageType: DS3.InfoContainer.ImageType.BigImage
            imageSource: "qrc:/resources/images/Athena/PD_compliant/ServiceSettings-PRO.svg"
            titleComponent.text: tr.make_sure_system_is_ready
            descComponent.text: tr.all_devices_should_be_added
        }

        DS3.Spacing {
            height: 36
        }

        DS3.Text {
            width: parent.width

            horizontalAlignment: Text.AlignHCenter
            style: ui.ds3.text.body.MBold
            text: {
                var locale = tr.get_locale()
                var link = "https://support.ajax.systems/" + locale + "/faqs/pd-6662-compliant-device-list/'"

                return util.hyperlink(tr.go_to_devices, link)
            }
        }
    }

    Parts.ButtonNextCancelPD {
        id: nextButton

        currentStep: 0

        button.onClicked: {
            advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/AlarmConfirmation.qml")
        }
    }
}
