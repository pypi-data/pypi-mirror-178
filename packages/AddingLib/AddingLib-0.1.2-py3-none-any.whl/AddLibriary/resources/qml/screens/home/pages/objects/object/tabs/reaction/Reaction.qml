import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"


Rectangle {
    id: reactionTab

    property bool isEditable: facility.editable_sections.includes("RAPID_RESPONSE_TEAMS")

    enabled: true
    color: ui.colors.black

    ColumnLayout {
        anchors.fill: parent
        spacing: 1

        Rectangle {
            color: ui.colors.dark3
            Layout.fillWidth: true
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48

            RowLayout {
                width: parent.width
                height: 48
                anchors {
                    bottom: parent.bottom
                    left: parent.left
                    leftMargin: 8
                }

                PanelTab {
                    id: allTab
                    text: tr.scenario_trigger_all
                    selected: true
                    Layout.alignment: Qt.AlignVCenter
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: ui.colors.dark3

            RowLayout {
                spacing: 0
                anchors.fill: parent

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Column {
                        anchors.centerIn: parent
                        spacing: 8

                        Custom.FontText {
                            text: tr.a911_main_group
                            color: ui.colors.middle1
                            font.pixelSize: 14
                        }

                        Repeater {
                            id: repeater
                            model: {
                                if (!facility.rapid_response_teams["primary_teams"]) return [null]
                                if (facility.rapid_response_teams["primary_teams"].length == 0) return [null]
                                return facility.rapid_response_teams["primary_teams"]
                            }

                            RowLayout {
                                width: 300
                                height: 48

                                spacing: 8

                                Connections {
                                    target: facility

                                    onRapid_response_teamsChanged: {
                                        if (!facility.rapid_response_teams["primary_teams"]) {
                                            repeater.model = [null]
                                            return
                                        }
                                        if (facility.rapid_response_teams["primary_teams"].length == 0) {
                                            repeater.model = [null]
                                            return
                                        }
                                        repeater.model = facility.rapid_response_teams["primary_teams"]
                                    }
                                }

                                Custom.ComboBox {
                                    id: primaryCombo
                                    enabled:  reactionTab.isEditable
                                    property var repeaterIndex: index
                                    currentIndex: -1
                                    model: []
                                    property var serverModel: []
                                    Layout.fillWidth: true
                                    Layout.minimumHeight: 40
                                    Layout.maximumHeight: 40
                                    textLabel.textFormat: Text.PlainText
                                    Component.onCompleted: {
                                        if (!facility.id) return

                                        update_server_model()
                                        if (repeater.model[index] && repeater.model[index] == null) {
                                            currentIndex = index
                                            return
                                        } else if (repeater.model[index]) {
                                            currentIndex = model_index(serverModel, repeater.model[index])
                                            return
                                        }
                                        currentIndex = -1
                                    }

                                    function model_index(model, item) {
                                        for(var i = 0; i < model.length; i++) {
                                            if (item && model[i] && item.id == model[i].id) {
                                                return i
                                            }
                                        }
                                        return -1
                                    }

                                    function update_server_model() {
                                        if (!facility.id || !companyAccess.OBJECT_CARD_REACTING) return

                                        var tempModel = app.fast_response_team_module.get_light_weight_rapid_response_teams()

                                        var newServerModel = []
                                        for (var i = 0; i < tempModel.length; i++) {
                                            var j = model_index(repeater.model, tempModel[i])
                                            var k = model_index(repeater_secondary.model, tempModel[i])
                                            if (j == -1 && k == -1) {
                                                newServerModel.push(tempModel[i])
                                                continue
                                            }
                                            if (j == index) {
                                                newServerModel.push(tempModel[i])
                                            }
                                        }

                                        var out = []
                                        for (var i = 0; i < newServerModel.length; i++) {
                                            out.push(newServerModel[i].name)
                                        }
                                        serverModel = newServerModel.slice()
                                        model = out.slice()
                                    }

                                    popup.onOpened: {
                                        update_server_model()
                                        if (repeater.model[index] && repeater.model[index] == null) {
                                            currentIndex = index
                                            return
                                        } else if (repeater.model[index]) {
                                            currentIndex = model_index(serverModel, repeater.model[index])
                                            return
                                        }
                                        currentIndex = -1
                                    }

                                    onActivated: {
                                        var item = serverModel[index]
                                        var new_model = repeater.model.slice(0, repeaterIndex).concat([item])
                                        new_model = new_model.concat(repeater.model.slice(repeaterIndex + 1, repeater.model.length))
                                        repeater.model = new_model
                                    }
                                }

                                Item {
                                    Layout.minimumHeight: 24
                                    Layout.maximumHeight: 24
                                    Layout.minimumWidth: 24
                                    Layout.maximumWidth: 24
                                    Image {
                                        width: 24
                                        height: 24

                                        anchors.centerIn: parent

                                        sourceSize.width: 40
                                        sourceSize.height: 40
                                        visible: reactionTab.isEditable && repeater.model.length > 1
                                        source: {
                                            return "qrc:/resources/images/icons/control-a-minus-button.svg"
                                        }
                                        // "resources/images/icons/control-a-minus-button.svg"
                                        // "resources/images/icons/control-a-plus-button.svg"

                                        Custom.HandMouseArea {
                                            anchors.fill: parent

                                            onClicked: {
                                                var new_model = repeater.model.slice(0, index).concat(repeater.model.slice(index + 1, repeater.model.length))
                                                repeater.model = new_model
                                            }
                                        }
                                    }
                                }
                            }
                        }


                        Item {
                            width: 300 - 24 - 8
                            height: 48
                            visible: reactionTab.isEditable
                            Rectangle {
                                width: 300 - 24 - 8
                                height: 40
                                radius: height / 2
                                color: ui.colors.dark1
                                anchors.centerIn: parent
                                visible: (repeater.model.length < 4)

                                Image {
                                    sourceSize.width: 40
                                    sourceSize.height: 40
                                    width: 24
                                    height: 24
                                    source: "qrc:/resources/images/icons/control-a-plus-button.svg"
                                    anchors.centerIn: parent

                                    Custom.HandMouseArea {
                                        onClicked: {
                                            var new_model = repeater.model.slice()
                                            new_model.push(null)
                                            repeater.model = new_model
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                Item {
                    Layout.minimumWidth: 1
                    Layout.maximumWidth: 1
                    Layout.fillHeight: true

                    Rectangle {
                        width: 1
                        height: parent.height - 200
                        color: ui.colors.dark2
                        anchors.centerIn: parent
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Column {
                        anchors.centerIn: parent
                        spacing: 8

                        Custom.FontText {
                            text: tr.a911_reserve_group
                            color: ui.colors.middle1
                            font.pixelSize: 14
                        }

                        Repeater {
                            id: repeater_secondary
                            model: {
                                if (!facility.rapid_response_teams["secondary_teams"]) return [null]
                                if (facility.rapid_response_teams["secondary_teams"].length == 0) return [null]
                                return facility.rapid_response_teams["secondary_teams"]
                            }

                            RowLayout {
                                width: 300
                                height: 48

                                spacing: 8

                                Connections {
                                    target: facility

                                    onRapid_response_teamsChanged: {
                                        if (!facility.rapid_response_teams["secondary_teams"]) {
                                            repeater_secondary.model = [null]
                                            return
                                        }
                                        if (facility.rapid_response_teams["secondary_teams"].length == 0) {
                                            repeater_secondary.model = [null]
                                            return
                                        }
                                        repeater_secondary.model = facility.rapid_response_teams["secondary_teams"]
                                    }
                                }

                                Custom.ComboBox {
                                    id: secondaryCombo
                                    enabled: reactionTab.isEditable
                                    property var repeaterIndex: index
                                    currentIndex: -1
                                    model: []
                                    property var serverModel: []
                                    Layout.fillWidth: true
                                    Layout.minimumHeight: 40
                                    Layout.maximumHeight: 40
                                    textLabel.textFormat: Text.PlainText
                                    Component.onCompleted: {
                                        if (!facility.id) return

                                        update_server_model()
                                        if (repeater_secondary.model[index] && repeater_secondary.model[index] == null) {
                                            currentIndex = index
                                            return
                                        } else if (repeater_secondary.model[index]) {
                                            currentIndex = model_index(serverModel, repeater_secondary.model[index])
                                            return
                                        }
                                        currentIndex = -1
                                    }

                                    function model_index(model, item) {
                                        for(var i = 0; i < model.length; i++) {
                                            if (item && model[i] && item.id == model[i].id) {
                                                return i
                                            }
                                        }
                                        return -1
                                    }

                                    function update_server_model() {
                                        if (!facility.id || !companyAccess.OBJECT_CARD_REACTING) return

                                        var tempModel = app.fast_response_team_module.get_light_weight_rapid_response_teams()

                                        var newServerModel = []
                                        for (var i = 0; i < tempModel.length; i++) {
                                            var j = model_index(repeater_secondary.model, tempModel[i])
                                            var k = model_index(repeater.model, tempModel[i])
                                            if (j == -1 && k == -1) {
                                                newServerModel.push(tempModel[i])
                                                continue
                                            }
                                            if (j == index) {
                                                newServerModel.push(tempModel[i])
                                            }
                                        }

                                        var out = []
                                        for (var i = 0; i < newServerModel.length; i++) {
                                            out.push(newServerModel[i].name)
                                        }
                                        serverModel = newServerModel.slice()
                                        model = out.slice()
                                    }

                                    popup.onOpened: {
                                        update_server_model()
                                        if (repeater_secondary.model[index] && repeater_secondary.model[index] == null) {
                                            currentIndex = index
                                            return
                                        } else if (repeater_secondary.model[index]) {
                                            currentIndex = model_index(serverModel, repeater_secondary.model[index])
                                            return
                                        }
                                        currentIndex = -1
                                    }

                                    onActivated: {
                                        var item = serverModel[index]
                                        var new_model = repeater_secondary.model.slice(0, repeaterIndex).concat([item])
                                        new_model = new_model.concat(repeater_secondary.model.slice(repeaterIndex + 1, repeater_secondary.model.length))
                                        repeater_secondary.model = new_model
                                    }
                                }

                                Item {
                                    Layout.minimumHeight: 24
                                    Layout.maximumHeight: 24
                                    Layout.minimumWidth: 24
                                    Layout.maximumWidth: 24
                                    Image {
                                        visible: reactionTab.isEditable && repeater_secondary.model.length > 1
                                        sourceSize.width: 40
                                        sourceSize.height: 40
                                        width: 24
                                        height: 24
                                        anchors.centerIn: parent
                                        source: {
                                            return "qrc:/resources/images/icons/control-a-minus-button.svg"
                                        }
                                        // "resources/images/icons/control-a-minus-button.svg"
                                        // "resources/images/icons/control-a-plus-button.svg"

                                        Custom.HandMouseArea {
                                            anchors.fill: parent

                                            onClicked: {
                                                var new_model = repeater_secondary.model.slice(0, index).concat(repeater_secondary.model.slice(index + 1, repeater_secondary.model.length))
                                                repeater_secondary.model = new_model
                                            }
                                        }
                                    }
                                }
                            }
                        }


                        Item {
                            width: 300 - 24 - 8
                            height: 48
                            visible: reactionTab.isEditable
                            Rectangle {
                                width: 300 - 24 - 8
                                height: 40
                                radius: height / 2
                                color: ui.colors.dark1
                                anchors.centerIn: parent
                                visible: (repeater_secondary.model.length < 4)

                                Image {
                                    sourceSize.width: 40
                                    sourceSize.height: 40
                                    width: 24
                                    height: 24
                                    source: "qrc:/resources/images/icons/control-a-plus-button.svg"
                                    anchors.centerIn: parent

                                    Custom.HandMouseArea {
                                        onClicked: {
                                            var new_model = repeater_secondary.model.slice()
                                            new_model.push(null)
                                            repeater_secondary.model = new_model
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            color: ui.colors.dark4
            Layout.fillWidth: true
            Layout.minimumHeight: 64
            Layout.maximumHeight: 64

            visible: {
                var bool1 = util.compare_jsons(facility.rapid_response_teams["primary_teams"], repeater.model)
                var bool2 = util.compare_jsons(facility.rapid_response_teams["secondary_teams"], repeater_secondary.model)
                return (!bool1 || !bool2)
            }

            RowLayout {
                id: row
                anchors.fill: parent

                function clear(repeater, model) {
                    if (!model) {
                        repeater.model = [null]
                        return
                    }
                    if (model.length == 0) {
                        repeater.model = [null]
                        return
                    }
                    repeater.model = model
                }

                Item {
                    Layout.fillWidth: true
                }

                Custom.Button {
                    Layout.preferredWidth: 296
                    Layout.preferredHeight: 48
                    color: ui.colors.green1
                    text: tr.save_scenario

                    onClicked: {
                        if (!facility.id) return

                        var teams = {}
                        teams["facility_id"] = facility.id
                        teams["primary_teams"] = repeater.model
                        teams["secondary_teams"] =  repeater_secondary.model
                        app.fast_response_team_module.save_facility_rapid_response_teams(teams)
                    }
                }

                Custom.Button {
                    Layout.preferredWidth: 296
                    Layout.preferredHeight: 48
                    color: ui.colors.white
                    transparent: true
                    text: tr.uncheck_all

                    onClicked: {
                        row.clear(repeater, facility.rapid_response_teams["primary_teams"])
                        row.clear(repeater_secondary, facility.rapid_response_teams["secondary_teams"])
                    }
                }

                Item {
                    Layout.fillWidth: true
                }
            }
        }
    }

    Connections {
        target: objectView

        onCurrentTabIndexChanged: {
            if (!facility.id) return

            if (currentTabIndex == 4) {
                app.fast_response_team_module.start_stream_object_rapid_response_teams(facility.id)
            }
        }
    }

    Component.onCompleted: {
        if (!facility.id) return

        if (currentTabIndex == 4) app.fast_response_team_module.start_stream_object_rapid_response_teams(facility.id)
    }
}
