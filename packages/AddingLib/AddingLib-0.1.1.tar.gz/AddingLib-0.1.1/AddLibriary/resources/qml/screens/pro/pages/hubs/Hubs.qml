import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/" as Root


Rectangle {
    id: hubsStack
    color: ui.ds3.bg.base

    property alias managementLoader: managementLoader

    function reloadHubIndices() {
        if (!hubsLoader.loadingNow) hubsContextLoader.contextTarget.getHubsIndices()
    }

    function updateFilter(value) {
        hubsContextLoader.contextTarget.filterString = value
    }

    function openHub(hub) {
        home.openOnNotificationsTab = ""

        application.debug("pro -> hubs -> dive into hub (id=" + hub.id + ")", false)
        __ga__.report("activity", "pro -> hubs -> dive into hub")

        hubsStack.startLoading()

        forceActiveFocus()
        appCompany.pro_hubs_model.subscribe(hub.id)
    }

    signal startLoading()
    signal stopLoading()

    Component.onCompleted: forceActiveFocus()

    Keys.onPressed: (event) => {
        hubsContextLoader.item.Keys.pressed(event)

        if (event.key == Qt.Key_F5) {
            home.reloadAllHubs()
        } else if (event.key == Qt.Key_Backspace && !!managementLoader.item) {
            application.debug("pro -> hubs -> hub -> back to all hubs")
            home.destroyHub()
        }
    }

    Root.ContextLoader {
        id: hubsContextLoader

        contextTarget: app.hubsView

        enabled: !managementLoader.item

        Connections {
            target: hubsContextLoader.item

            onHubChoosen: (hub) => {
                openHub(hub)
                app.hubsView.chooseHub(hub.id, appUser.cluster_user_id)
            }
        }
    }

    Root.ContextLoader {
        id: hubsSidebarContextLoader

        width: childrenRect.width
        height: visible ? parent.height : 0

        contextTarget: !!managementLoader.item && __new_hubs_sidebar_features__ ? app.hubsView.hubsListSidebar : null

        Connections {
            target: hubsSidebarContextLoader.item

            onHubChosen: (hub) => {
                appCompany.pro_hubs_model.unsubscribe()
                app.hubsView.chooseHub("", "")
                openHub(hub)
                app.hubsView.chooseHub(hub.id, appUser.cluster_user_id)
            }
        }
    }

    Loader {
        id: managementLoader
        source: ""
        anchors {
            fill: parent
            leftMargin: __new_hubs_sidebar_features__ ? hubsSidebarContextLoader.width : 0
        }
    }

    Custom.BlockLoading {
        id: hubsLoader
        radius: 32
        minTime: 500
        customOpacity: 0.1
        startSignals: [home.reloadAllHubs, app.rpc.hubConfig.hubRequested]
        stopSignals: [hubsStack.stopLoading, app.hubReceived, app.hubNotReceived]
    }

    Connections {
        target: app.rpc.hubs
        onRequestHubsIndices: {
            startLoading()
        }
        onIncomingHubsIndices: {
            stopLoading()
        }
        onIncomingHubsIndicesFailed: {
            stopLoading()
        }
    }

    Connections {
        target: app.hub_management_module

        onBindHubToUserSuccess: {
            home.reloadAllHubs()
        }
    }

    Connections {
        target: app

        onHubReceived: {
            managementLoader.setSource("qrc:/resources/qml/screens/pro/pages/hubs/hub/Hub.qml")
        }
    }
}
