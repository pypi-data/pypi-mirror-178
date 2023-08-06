import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: eventsStack
    color: ui.colors.black

    property alias eventsSidebar: eventsSidebar

    signal newEventClick(string href, variant color, variant event, string itemType)

    RowLayout {
        anchors.fill: parent
        spacing: 10

        EventsSidebar {
            id: eventsSidebar
            Layout.maximumWidth: 334
            Layout.minimumWidth: 334
            Layout.fillHeight: true
        }

        EventsBody {
            id: eventsBody
            Layout.alignment: Qt.AlignRight
            Layout.fillHeight: true
            Layout.fillWidth: true
        }
    }

    Custom.BlockLoading {
        startSignals: [eventsSidebar.blockElement, app.getAppChangeLogLoadingStarted, app.getCompanyHubPermissionDurationLoadingStarted]
        stopSignals: [appCompany.events_model.dataReceived, appCompany.events_model.dataNotReceived, app.whatsNew, app.companyHubPermissionDurationReceived]
    }
}
