import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13


Rectangle {
    id: objectView
    anchors.fill: parent
    color: ui.colors.black

    property var fullView: false
    property var currentTabIndex: 0

    property var functionalSettingsOn: {
        if (!appCompany) return false
        if (!appCompany.workplaces_model) return false
        if (!appCompany.workplaces_model.incidents_settings) return false
        if (!appCompany.workplaces_model.incidents_settings.facility_permission_settings) return false
        if (!appCompany.workplaces_model.incidents_settings.facility_permission_settings.full_access) return false

        if (appCompany.workplaces_model.incidents_settings.facility_permission_settings.full_access == "ON") return true
        return false
    }

    onFunctionalSettingsOnChanged: {
        if (objectView.currentTabIndex == 6) objectView.currentTabIndex = 0
    }

    property var installationEnabled: appCompany.data.provided_services.installation

    onInstallationEnabledChanged: {
        if (objectView.currentTabIndex == 6 && !installationEnabled) objectView.currentTabIndex = 0
    }

    RowLayout {
        anchors.fill: parent
        spacing: 8

        SidebarList {
            Layout.fillHeight: true
            Layout.minimumWidth: 334
            Layout.maximumWidth: 334
        }

        Loader {
            id: objectLoader
            Layout.fillHeight: true
            Layout.fillWidth: true

            Component.onCompleted: {
                setSource("qrc:/resources/qml/screens/home/pages/objects/object/Object.qml")
                aliasObjectLoader = objectLoader
            }
        }

        Item {
            Layout.preferredWidth: 1
        }
    }

    Component.onCompleted: {
        if (companyAccess.COMPANY_SERVICES_SETTINGS && appCompany.data.provided_services.installation) {
            app.company_module.get_company_settings()
        }
    }
}
