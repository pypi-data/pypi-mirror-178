import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/pro/pages/company/components" as Desktop


Item {
    id: companyCreatedScreen

    property var companyInfo: null

    function loginIntoCompany() {
        if (!companyCreatedScreen.companyInfo) return
        if (!companyCreatedScreen.companyInfo.id) return

        application.debug("pro -> company -> go to the new company")
        app.login_module.login_into_company_tab(companyCreatedScreen.companyInfo.id, "OWNER", "objects")
    }

    Desktop.InfoScreenHeader {
        id: infoScreenHeader

        width: parent.width * 0.7

        icon: "qrc:/resources/images/pro/company/accepted.svg"
        title: tr.new_company_success_pro_desktop_title
        subtitle: {
            if (!companyCreatedScreen.companyInfo) return util.insert(tr.new_company_success_pro_desktop_description, [""])
            if (!companyCreatedScreen.companyInfo.email_addresses) return util.insert(tr.new_company_success_pro_desktop_description, [""])
            if (!companyCreatedScreen.companyInfo.email_addresses[0]) return util.insert(tr.new_company_success_pro_desktop_description, [""])
            if (!companyCreatedScreen.companyInfo.email_addresses[0].email) return util.insert(tr.new_company_success_pro_desktop_description, [""])

            return util.insert(tr.new_company_success_pro_desktop_description, [companyCreatedScreen.companyInfo.email_addresses[0].email])
        }

        buttonText: tr.button_go_to_objects
        buttonAction: companyCreatedScreen.loginIntoCompany

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
