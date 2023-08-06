import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: monitoringCompanies

    Component.onCompleted: {
        if (companyAccess.OBJECT_CARD_MONITORING_COMPANIES) {
            app.company_module.get_monitoring_companies(facility.hub_id, management)
        }
    }

    height: parent.height

    color: ui.ds3.bg.base

    DS3.ScrollView {
        padding: 32

        ListView {
            id: listView

            width: parent.width
            height: contentHeight

            interactive: false
            spacing: 1

            model: management.monitoring_companies
            delegate: CompanyDelegate {}
        }
    }

    NoCompanies {
        id: noCompaniesBanner

        visible: false
    }

    Connections {
        target: management.monitoring_companies

        onMonitoringCompaniesChanged: {
            noCompaniesBanner.visible = !management.monitoring_companies.length
        }
    }
}
