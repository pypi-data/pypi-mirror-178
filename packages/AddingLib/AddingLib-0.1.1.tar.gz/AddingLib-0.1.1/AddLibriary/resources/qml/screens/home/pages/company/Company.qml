import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/screens/home/pages/company/info"
import "qrc:/resources/qml/screens/home/pages/company/settings"
import "qrc:/resources/qml/screens/home/pages/company/access_rights"
import "qrc:/resources/qml/screens/home/pages/company/staff"
import "qrc:/resources/qml/screens/home/pages/company/workplaces"
import "qrc:/resources/qml/screens/home/pages/company/gbr"
import "qrc:/resources/qml/screens/home/pages/company/bindings"
import "qrc:/resources/qml/components/911" as Custom


Loader {
    id: company

    property bool editModeOpened: false

    signal editModeOpen

    Component.onCompleted: {
        if (companyAccess.COMPANY) {
            sourceComponent = component
        }
    }

    Component {
        id: component

        Rectangle {
            id: companyStack
            color: ui.colors.black

            property var firstVisibleIndex: 0
            property var lastVisibleIndex: 6

            property var currentIndex: -1

            property var companyEditMode: false

            onCompanyEditModeChanged: currentIndexChanged()
            onCurrentIndexChanged: company.editModeOpened = companyEditMode && currentIndex == 0

            function getFirstIndex() {
                var idx = 0

                if (!companyAccess.COMPANY_GENERAL_INFO) idx++
                else return idx

                if (!companyAccess.COMPANY_SERVICES_SETTINGS) idx++
                else return idx

                if (!(__phod_company_features__ && __maintenance_report_features__) && !companyAccess.EMPLOYEE_ROLES_ACCESS_RIGHTS) idx++  //access_rights
                else return idx

                if (!companyAccess.COMPANY_EMPLOYEES) idx++
                else return idx

                if (!companyAccess.COMPANY_WORKPLACES) idx++
                else return idx

                if (!companyAccess.COMPANY_RRU) idx++
                else return idx

                if (!companyAccess.COMPANY_HUBS) idx++
                else return idx

                return idx
            }

            function getLastIndex() {
                var idx = 5

                if (!companyAccess.COMPANY_HUBS) idx--
                else return idx

                if (!companyAccess.COMPANY_RRU) idx--
                else return idx

                if (!(__phod_company_features__ || __maintenance_report_features__)) idx--   // access_rights
                else return idx

                if (!companyAccess.COMPANY_WORKPLACES) idx--
                else return idx

                if (!companyAccess.COMPANY_EMPLOYEES) idx--
                else return idx

                if (!companyAccess.COMPANY_SERVICES_SETTINGS) idx--
                else return idx

                if (!companyAccess.COMPANY_GENERAL_INFO) idx--
                else return idx

                return idx
            }

            function getAvailableTabs() {
                var availableTabs = []

                if (companyAccess.COMPANY_GENERAL_INFO) availableTabs.push("MainInfo")
                if (companyAccess.COMPANY_SERVICES_SETTINGS) availableTabs.push("FunctionalSettings")
                if (__phod_company_features__ || __maintenance_report_features__) availableTabs.push("AccessRights")
                if (companyAccess.COMPANY_EMPLOYEES) availableTabs.push("Staff")
                if (companyAccess.COMPANY_WORKPLACES) availableTabs.push("Workplaces")
                if (companyAccess.COMPANY_RRU) availableTabs.push("Gbr")
                if (companyAccess.COMPANY_HUBS) availableTabs.push("Bindings")

                return availableTabs
            }

            property var installationEnabled: appCompany.data.provided_services.installation

            onInstallationEnabledChanged: {
                companyStack.firstVisibleIndex = companyStack.getFirstIndex()
                companyStack.lastVisibleIndex = companyStack.getLastIndex()

                var availableTabs = companyStack.getAvailableTabs()
                if (companyTabsLoader.item && currentTab) {
                    var currentTab = companyTabsLoader.item.currentTab
                }
                if (companyTabsLoader.item && currentTab && availableTabs.includes(currentTab)) {
                    companyStack.currentIndex = availableTabs.indexOf(currentTab)
                    return
                }
                companyStack.currentIndex = companyStack.firstVisibleIndex
            }

            Component.onCompleted: {
                companyStack.firstVisibleIndex = companyStack.getFirstIndex()
                companyStack.lastVisibleIndex = companyStack.getLastIndex()
                companyStack.currentIndex = companyStack.firstVisibleIndex
            }

            Loader {
                id: companyTabsLoader

                anchors.fill: parent
                Component.onCompleted: {
                    if (companyAccess.COMPANY) sourceComponent = companyComponent
                }
            }

            Component {
                id: companyComponent
                ColumnLayout {
                    anchors.fill: parent

                    property var currentTab: ["MainInfo", "FunctionalSettings", "AccessRights", "Staff",  "Workplaces", "Gbr", "Bindings"][stackLayout.currentIndex]

                    RowLayout {
                        spacing: 10
                        Layout.fillWidth: true

                        CompanySidebar {
                            Layout.maximumWidth: 334
                            Layout.minimumWidth: 334
                            Layout.fillHeight: true
                        }

                        StackLayout {
                            id: stackLayout
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                            currentIndex: companyStack.currentIndex

                            MainInfo {}
                            FunctionalSettings {}
                            AccessRights {}
                            Staff {}
                            Workplaces {}
                            Gbr {}
                            Bindings {}
                        }
                    }
                }
            }

            Connections {
                target: company

                onEditModeOpen: currentIndex = 0
            }
        }
    }
}