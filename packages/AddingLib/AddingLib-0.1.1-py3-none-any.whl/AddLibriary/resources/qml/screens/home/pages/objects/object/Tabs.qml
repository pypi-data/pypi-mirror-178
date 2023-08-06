import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/object/tabs"
import "qrc:/resources/qml/screens/home/pages/objects/object/tabs/monitoring_companies"
import "qrc:/resources/qml/screens/home/pages/objects/object/tabs/responsible"
import "qrc:/resources/qml/screens/home/pages/objects/object/tabs/reaction"
import "qrc:/resources/qml/screens/home/pages/objects/object/tabs/plans"
import "qrc:/resources/qml/screens/home/pages/objects/object/tabs/logs"
import "qrc:/resources/qml/screens/home/pages/objects/object/tabs/equipment"
import "qrc:/resources/qml/screens/home/pages/objects/object/tabs/additional_info"
import "qrc:/resources/qml/screens/home/pages/objects/object/tabs/installers"


Rectangle {
    color: ui.colors.black
    Layout.fillWidth: true
    Layout.fillHeight: true

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Rectangle {
            id: tabsHeader
            color: ui.colors.black
            Layout.fillWidth: true
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48

            Row {
                anchors.fill: parent

                Repeater {
                    id: repeater
                    model: {
                        let m = []
                        if (companyAccess.OBJECT_CARD_EQUIPMENT) m.push({key: "a911_equipment", stackIndex: 0})
                        if (companyAccess.OBJECT_CARD_MONITORING_COMPANIES) m.push({key: "monitoring_companies_list_title", stackIndex: 1})
                        if (companyAccess.OBJECT_CARD_CONTACT_PERSONS) m.push({key: "a911_responsible", stackIndex: 2})
                        if (companyAccess.OBJECT_CARD_OBJECT_PHOTOS) m.push({key: "a911_plan", stackIndex: 3})
                        if (companyAccess.OBJECT_CARD_REACTING) m.push({key: "a911_reaction", stackIndex: 4})
                        if (companyAccess.OBJECT_CARD_NOTES) m.push({key: "a911_additional_info", stackIndex: 5})
                        if (companyAccess.OBJECT_CARD_LOG) m.push({key: "a911_log", stackIndex: 6})
                        if (
                            companyAccess.OBJECT_CARD_INSTALLERS
                            && facility.data.provided_services.includes("INSTALLATION")
                            && !!appCompany
                            && !!appCompany.workplaces_model
                            && !!appCompany.workplaces_model.incidents_settings
                            && !!appCompany.workplaces_model.incidents_settings.facility_permission_settings
                            && appCompany.workplaces_model.incidents_settings.facility_permission_settings.full_access != "ON"
                        ) m.push({key: "installers", stackIndex: 7})
                        return m
                    }

                    Rectangle {
                        id: tabBarRect
                        color: repeater.model[index].stackIndex == currentTabIndex ? ui.colors.dark3 : ui.colors.black
                        enabled: {
                            if (!facility || !facility.data || !facility.data.company_id) return false
                            return facility.id ? true : false
                        }
                        width: {
                            return tabsHeader.width / repeater.model.length
                        }
                        height: 48

                        Custom.FontText {
                            text: tr[repeater.model[index].key]
                            font.pixelSize: 14
                            color: repeater.model[index].stackIndex == currentTabIndex ? ui.colors.light1 : ui.colors.middle3
                            wrapMode: Text.WordWrap
                            width: tabBarRect.width
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                            anchors.centerIn: parent
                        }

                        Custom.HandMouseArea {
                            anchors.fill: parent
                            onClicked: {
                                currentTabIndex = repeater.model[index].stackIndex
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            id: tabsView
            color: ui.colors.dark2
            Layout.fillWidth: true
            Layout.fillHeight: true

            property var tabsMonitoringRequested: {
                if (!facility) return false
                if (!facility.data) return false
                if (!facility.data.status) return false

                return facility.data.status == "MONITORING_REQUESTED"
            }

            StackLayout {
                id: facilityStackLayout

                anchors.fill: parent
                currentIndex: currentTabIndex

                Equipment {}
                MonitoringCompanies {}
                Responsible {}
                Plans {}
                Reaction {}
                AdditionalInfo {}
                Log {}
                Installers {}
            }
        }
    }
}
