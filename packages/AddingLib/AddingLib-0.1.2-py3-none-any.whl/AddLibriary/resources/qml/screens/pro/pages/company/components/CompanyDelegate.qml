import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    width: parent.width
    height: Math.max(120, 40 + companyNameBlock.height + 8 + companyInfoBlock.height)

    property var currentCompany: null

    enabled: currentCompany && currentCompany.available
    opacity: enabled ? 1 : 0.5

    Desktop.OriginalImage {
        id: imageItem

        size: 84
        radius: 8
        text: companyNameText.text
        trueImage: currentCompany && currentCompany.logo_url ? currentCompany.logo_url : ""

        anchors {
            top: parent.top
            left: parent.left
        }
    }

    Item {
        id: companyButtonBlock

        width: companyButton.textButton.contentWidth + 64
        height: 48

        anchors {
            top: parent.top
            right: parent.right
        }

        Custom.Button {
            id: companyButton

            width: parent.width
            text: currentCompany && currentCompany.available ? tr.button_my_company_merge : tr.button_company_already_registered

            animColor: color
            transparent: true
            color: ui.colors.white
            loading_background_color: "transparent"
            textButton.textFormat: Text.PlainText

            anchors.centerIn: parent

            onClicked: {
                var settings = {
                    "cluster_company_id": currentCompany.cluster_company_id
                }

                if (currentCompany.cluster_company_id.toLowerCase() in companyStack.confirmedEmails) {
                    settings["email_token"] = companyStack.confirmedEmails[currentCompany.cluster_company_id.toLowerCase()]

                    companyButton.loading = true
                    app.company_module.get_company_for_merge(settings)
                    return
                }

                var td = companyStack.timeDiff(currentCompany.cluster_company_id)
                if (td > 0) {
                    var confirmationInfo = companyStack.sendCodesInfo[currentCompany.cluster_company_id]
                    Popups.confirm_email_popup(confirmationInfo, companyStack, true)
                    return
                }

                companyButton.loading = true
                app.company_module.request_company_email_access_confirmation(settings)
            }
        }

        Connections {
            target: app.company_module

            onRequestCompanyEmailAccessConfirmationSuccess: {
                companyButton.loading = false
            }

            onRequestCompanyEmailAccessConfirmationFailed: {
                companyButton.loading = false
            }

            onGetCompanyForMergeSuccess: {
                companyButton.loading = false
            }

            onGetCompanyForMergeFailed: {
                companyButton.loading = false
            }
        }
    }

    Item {
        id: companyNameBlock

        width: parent.width - 108 - companyButtonBlock.width - 16
        height: companyNameItem.height

        anchors {
            top: parent.top
            left: imageItem.right
            leftMargin: 24
        }

        Item {
            id: companyNameItem

            width: parent.width
            height: companyNameText.contentHeight

            Desktop.NormalText {
                id: companyNameText

                text: currentCompany && currentCompany.company_name ? currentCompany.company_name : ""
                color: ui.colors.light3
                size: 24
                bold: true

                anchors.fill: parent
            }
        }
    }

    Column {
        id: companyInfoBlock

        spacing: 2
        width: parent.width - 108 - companyButtonBlock.width - 16

        anchors {
            top: companyNameBlock.bottom
            topMargin: 8
            left: imageItem.right
            leftMargin: 24
        }

        Item {
            id: companyNumberItem

            width: parent.width
            height: visible ? companyNumberText.contentHeight : 0

            visible: companyNumberText.text

            Desktop.NormalText {
                id: companyNumberText

                text: currentCompany && currentCompany.phone_number ? currentCompany.phone_number : ""
                color: ui.colors.middle1
                size: 12
                elideMode: true

                anchors.fill: parent
            }
        }

        Item {
            id: companyUrlItem

            width: parent.width
            height: visible ? companyUrlText.contentHeight : 0

            visible: companyUrlText.text

            Desktop.NormalText {
                id: companyUrlText

                text: currentCompany && currentCompany.web_site_url ? currentCompany.web_site_url : ""
                color: ui.colors.middle1
                size: 12
                elideMode: true

                anchors.fill: parent
            }
        }

        Item {
            width: parent.width
            height: 4

            visible: companyNumberItem.visible || companyUrlItem.visible
        }

        Item {
            id: companyLocationsItem

            width: parent.width
            height: visible ? companyLocationsText.contentHeight : 0

            visible: companyLocationsText.text

            Desktop.NormalText {
                id: companyLocationsText

                text: currentCompany && currentCompany.locationsString ? currentCompany.locationsString : ""
                color: ui.colors.middle1
                size: 12
                elideMode: true

                anchors.fill: parent
            }
        }
    }

    Rectangle {
        width: parent.width
        height: 1

        color: ui.colors.middle4

        anchors.bottom: parent.bottom
    }
}
