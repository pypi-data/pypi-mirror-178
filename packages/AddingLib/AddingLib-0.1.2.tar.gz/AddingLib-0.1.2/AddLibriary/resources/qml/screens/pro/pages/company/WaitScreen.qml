import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: companyWaitScreen

    property var mode: "waiting"
    property var companyId: ""
    property var companyInfo: null

    function goToHubs() {
        application.debug("pro -> sidebar -> open hubs tab")
        header.currentState = 0
        header.sidebarVisible = false
    }

    function tryAgain() {
        companyLoader.setSource(companyStack.startScreen)
    }

    function loginIntoCompany() {
        if (!companyWaitScreen.companyId) return

        application.debug("pro -> company -> go to the new company")
        app.login_module.login_into_company_tab(companyWaitScreen.companyId, "OWNER", "objects")
    }

    Connections {
        target: app.company_module

        onCompanyStatusChanged: {
            if (status == "ACCEPTED") {
                companyWaitScreen.companyId = company_id
                companyWaitScreen.mode = "accepted"
            }

            if (status == "REJECTED") {
                companyWaitScreen.mode = "rejected"
            }
        }
    }

    Desktop.InfoScreenHeader {
        id: infoScreenHeader

        width: parent.width * 0.7

        icon: {
            if (companyWaitScreen.mode == "accepted") return "qrc:/resources/images/pro/company/accepted.svg"
            if (companyWaitScreen.mode == "rejected") return "qrc:/resources/images/pro/company/rejected.svg"
            return "qrc:/resources/images/pro/company/waiting.svg"
        }

        title: {
            if (companyWaitScreen.mode == "accepted") return tr.new_company_success_pro_desktop_title
            if (companyWaitScreen.mode == "rejected") return tr.a911_company_create_request_rejected_short

            if (companyWaitScreen.companyInfo) return tr.merge_success_pro_desktop_title
            return tr.merge_review_pro_desktop_title

            /*
                accepted:
                    tr.a911_company_create_request_approved_short
                    tr.new_company_success_pro_desktop_title

                waiting:
                    tr.a911_company_create_request_created_short
                    tr.merge_success_pro_desktop_title
                    tr.merge_review_pro_desktop_title
            */
        }
        subtitle: {
            var support = ["<style>a:link { color: '#5ae4aa'; text-decoration: none; }</style><u><a href='https://support.ajax.systems/" + tr.locale + "/for-users/'>", "</a></u>"]

            if (companyWaitScreen.mode == "accepted") return tr.new_company_success_pro_desktop_description
            if (companyWaitScreen.mode == "rejected") return tr.a911_company_create_request_rejected + " " + support[0] + tr.support_sercive_link + support[1]

            if (companyWaitScreen.companyInfo) return util.hyperlink(tr.merge_success_pro_desktop_description, "mailto:support@ajax.systems")
            return util.hyperlink(tr.merge_review_pro_desktop_info, "mailto:support@ajax.systems")

            /*
                accepted:
                    tr.a911_company_create_request_approved
                    tr.new_company_success_pro_desktop_description

                waiting:
                    tr.a911_company_create_request_created
                    tr.merge_success_pro_desktop_description
                    tr.merge_review_pro_desktop_info
            */
        }

        buttonText: {
            if (companyWaitScreen.mode == "accepted") return tr.button_go_to_objects
            if (companyWaitScreen.mode == "rejected") return tr.a911_create_company_after_reject
            return tr.button_go_to_hubs
        }
        buttonAction: {
            if (companyWaitScreen.mode == "accepted") return companyWaitScreen.loginIntoCompany
            if (companyWaitScreen.mode == "rejected") return companyWaitScreen.tryAgain
            return companyWaitScreen.goToHubs
        }

        titleColor: {
            if (companyWaitScreen.mode == "accepted") return ui.colors.white
            if (companyWaitScreen.mode == "rejected") return ui.colors.red1
            return ui.colors.white
        }

        anchors {
            top: parent.top
            topMargin: (moreAboutDesktop.y - height) / 4
            horizontalCenter: parent.horizontalCenter
        }
    }

    Desktop.MoreAboutDesktop {
        id: moreAboutDesktop

        width: parent.width * 0.7

        anchors {
            bottom: parent.bottom
            bottomMargin: 64
            horizontalCenter: parent.horizontalCenter
        }
    }
}
