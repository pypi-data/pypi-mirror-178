import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911" as Custom


Rectangle {
    color: ui.colors.dark3

    Custom.EmptySpaceLogo {
        size: parent.width / 2
        visible: responsibleViewLoader.source == ""
    }

    function load() {
        if (currentResponsibleIndex == -1) {
            responsibleViewLoader.source = ""
            return
        }
        var source = "qrc:/resources/qml/screens/home/pages/objects/object/tabs/responsible/"
        source += responsibleViewLoader.editMode ? "EditInfo.qml" : "StaticInfo.qml"
        responsibleViewLoader.setSource(source, {"currentObject": currentResponsibleObject})
    }

    Loader {
        id: responsibleViewLoader
        anchors.fill: parent

        property var editMode: false

        onEditModeChanged: load()
    }

    Connections {
        target: responsibleTab

        onCurrentResponsibleIndexChanged: {
            if (responsibleViewLoader.editMode) {
                responsibleViewLoader.editMode = false
                return
            }
            load()
        }
    }

    Connections {
        target: appCompany.current_facility ? appCompany.current_facility.responsible_persons : null

        onForcePersonUpdate: {
            if (currentResponsibleIndex != index) return
            currentResponsibleObject = appCompany.current_facility.responsible_persons.get(index)
            if (!responsibleViewLoader.editMode) load()
        }

        onPersonDeleted: {
            if (responsible_id == currentResponsibleObject.id) {
                responsibleTab.currentResponsibleIndex = -1
                responsibleTab.currentResponsibleObject = null
            }
        }
    }
}