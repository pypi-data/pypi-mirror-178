import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: objectsStack

    property alias objectsScreenLoaderSource: objectsScreenLoader.source
    property alias screenEnable: objectsScreenLoader.item
    property var objectsSidebar: !!objectsScreenLoader.item ? objectsScreenLoader.item.sidebar : null
    property var currentObjectIndex: -1
    property var aliasObjectLoader: null
    property var hubHexId: ""
    property var currentMode: objectsSidebar.currentTab.mode

    signal startLoading()

    color: ui.colors.black

    Connections {
        target: app

        onFacilityReceived: {
            if (currentObjectIndex == index) return
            currentObjectIndex = index

            if (currentObjectIndex == -5) app.change_screen()
        }
    }

    onCurrentObjectIndexChanged: {
        if (currentObjectIndex == -1) {
            objectsScreenLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/Objects.qml")
            app.facility_module.clear_facility()
            screenEnable.enableState = true
        } else if (currentObjectIndex == -4) {
            objectsScreenLoader.setSource("")
            app.facility_module.clear_facility()
            app.facility_module.clear_model()
            if (!!screenEnable) screenEnable.enableState = true
        } else {
            if (!!screenEnable && !screenEnable.enableState) {
                aliasObjectLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/Object.qml")
                return
            }
            objectsScreenLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/ObjectView.qml", {"currentMode": currentMode})
            if (!!screenEnable && screenEnable.enableState != undefined) screenEnable.enableState = false
        }
    }

    Custom.BlockLoading {
        minTime: 300
        startSignals: [objectsStack.startLoading]
        stopSignals: [app.facilityReceived, app.facilityNotReceived]
    }

    Loader {
        id: objectsScreenLoader

        z: 0
        anchors.fill: parent

        sourceComponent: loadComponent
    }

    Component {
        id: loadComponent

        Rectangle {
            id: objectsScreen

            color: ui.colors.black

            property bool enableState: true
            property alias sidebar: objectsSidebar

            /*
            0, 1, ...   - true indexes
            -1   - return to objects with model & counters reload
            -2   - sidebar facilities list has no selected facility item
            -3   - go to facility & open edit mode (access is allowed)
            -4   - return to objects without reload
            -5   - go to facility & change screen to Objects tab (force)
            */

            Component.onCompleted: {
                objectsSidebar.reloadModel()
            }

            RowLayout {
                id: layout
                anchors.fill: parent
                spacing: 8
                z: 0
                enabled: enableState

                Categories {
                    id: objectsSidebar

                    Layout.maximumWidth: 334
                    Layout.minimumWidth: 334
                    Layout.fillHeight: true
                }

                ObjectsBody {
                    id: objectsBody

                    Layout.alignment: Qt.AlignRight
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                }

                Item {
                    Layout.preferredWidth: 1
                }
            }
        }
    }
}
