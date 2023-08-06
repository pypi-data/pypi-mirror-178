import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"


AjaxPopup {
    id: popup
    objectName: "facilitiesSearchPopup"
    width: application.width / 2
    height: application.height - 80
    closePolicy: Popup.CloseOnEscape

    modal: true
    focus: true

    anchors.centerIn: parent

    onOpened: {
        searchField.control.forceActiveFocus(true)
    }

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.8  // 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y

        Image {
            source: "qrc:/resources/images/icons/a-delete-button.svg"
            sourceSize.width: 56
            sourceSize.height: 56
            anchors {
                top: parent.top
                topMargin: 32
                right: parent.right
                rightMargin: 32
            }

            Custom.HandMouseArea {
                onClicked: {
                    popup.close()
                }
            }
        }
    }

    property var todo: null
    property var objectsStack: null

    property var searchedModel: appCompany.searched_objects_model.filtered

    property var searching: false

    Connections {
        target: appCompany.searched_objects_model

        onSearchEnded: {
            popup.searching = false

            if (searchedModel.length == 0 && searchField.prevPhrase == searchField.control.text && searchField.prevPhrase != "") searchField.notFound = true
        }
    }

    Connections {
        target: app.facility_module

        onSearchError: {
            if (result["1"]) {
                Popups.text_popup(tr.error, result["1"].message)
            }
        }
    }

    contentItem: Item {
        anchors.fill: parent

        MouseArea {
            anchors.fill: parent
        }

        Item {
            id: searchFieldItem
            width: parent.width
            height: 40
            anchors {
                top: parent.top
                topMargin: 96
                horizontalCenter: parent.horizontalCenter
            }

            MouseArea {
                anchors.fill: parent
            }

            Custom.SearchField {
                id: searchField
                width: parent.width
                height: 40
                anchors.centerIn: parent
                placeHolderText: tr.a911_search
                color: ui.colors.dark2
                radius: (control.activeFocus || !valid) ? 0 : 10
                border.width: (control.activeFocus || !valid) ? 1 : 0
                border.color: valid ? ui.colors.green3 : ui.colors.red3
                ico.anchors.rightMargin: 12
                control.leftPadding: 16
                control.rightPadding: notFound ? Math.max(56 + notFoundText.width, parent.width - searchField.control.contentWidth - notFoundText.width) : 44
                clearing: false
                action: searchField.searchFacilities

                property var notFound: false

                control.onTextChanged: {
                    if (!valid) valid = true
                    notFound = false
                }

                control.onActiveFocusChanged: {
                    if (!valid) valid = true
                }

                property var prevPhrase: ""

                function searchFacilities() {
                    if (control.text.length == 1) {
                        searchField.control.focus = false
                        prevPhrase = ""
                        app.facility_module.search_facilities("")
                        searchField.valid = false
                        return
                    }

                    if (control.text == prevPhrase) return
                    popup.searching = true
                    prevPhrase = control.text
                    app.facility_module.search_facilities(control.text)
                }

                Keys.onEnterPressed: {
                    searchField.searchFacilities()
                }

                Keys.onReturnPressed: {
                    var dummy = searchField.searchFacilities()
                    if (popup.searchedModel.length == 1) {
                        function action(tempId) {
                            var index = 0
                            searchedModel.reload_objects_model(index)

                            var tempIndex = searchedModel.get_section_index(index)
                            function inner() {
                                objectsStack.startLoading()
                                if (appCompany.current_facility && tempIndex == objectsStack.currentObjectIndex) {
                                    objectsStack.currentObjectIndex = -2
                                }
                                app.facility_module.get_facility(tempId, tempIndex)
                            }

                            return inner
                        }
                        var _id = searchedModel.get_first_object_id()
                        popup.todo = action(_id)
                        popup.close()

                    }
                }

                Custom.FontText {
                    id: notFoundText
                    width: contentWidth
                    text: "—  " + tr.no_results_found
                    color: ui.colors.middle3
                    visible: searchField.notFound
                    font.pixelSize: 12
                    font.weight: Font.Light
                    wrapMode: Text.NoWrap
                    horizontalAlignment: Text.AlignRight
                    anchors {
                        right: parent.right
                        rightMargin: Math.max(48, parent.width - searchField.control.contentWidth - notFoundText.width - 24)
                        verticalCenter: parent.verticalCenter
                    }
                }
            }
        }

        Custom.FontText {
            id: hintText
            visible: searchField.valid && listView.model.length == 0
            text: util.insert(tr.search_syntax_help, ["<br>", "<br>"])
            width: parent.width
            color: ui.colors.white
            opacity: 0.5
            font.pixelSize: 14
            font.weight: Font.Light
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignLeft
            anchors {
                top: searchFieldItem.bottom
                topMargin: 24
                left: parent.left
                leftMargin: 24
            }
        }

        Custom.FontText {
            id: errorText
            visible: !searchField.valid
            text: tr.minimum_2_characters_to_search
            width: parent.width
            color: ui.colors.red2
            font.pixelSize: 14
            font.weight: Font.Light
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignLeft
            anchors {
                top: searchFieldItem.bottom
                topMargin: 24
                left: parent.left
                leftMargin: 24
            }
        }

        Rectangle {
            visible: searchedModel.length > 0
            width: parent.width
            height: listView.contentHeight + 16 < parent.height - 144 ? listView.contentHeight + 16 : parent.height - 144
            radius: 8
            color: ui.colors.dark3
            anchors {
                top: searchFieldItem.bottom
                topMargin: 8
            }

            ListView {
                id: listView
                clip: true
                spacing: 0
                width: parent.width
                height: parent.height - 16
                headerPositioning: ListView.OverlayHeader
                boundsBehavior: Flickable.StopAtBounds
                anchors.verticalCenter: parent.verticalCenter

                ScrollBar.vertical: Custom.ScrollBar {}

                model: popup.searchedModel

                section.property: "unit"
                section.criteria: ViewSection.FullString
                section.labelPositioning: ViewSection.CurrentLabelAtStart | ViewSection.InlineLabels
                section.delegate: Rectangle {
                    width: parent.width
                    height: 32
                    color: ui.colors.dark3

                    Custom.FontText {
                        width: parent.width - 48
                        height: contentHeight
                        color: ui.colors.middle2
                        verticalAlignment: Text.AlignVCenter
                        anchors {
                            left: parent.left
                            leftMargin: 24
                            verticalCenter: parent.verticalCenter
                        }

                        text: {
                            if (section == "registration_number") return tr.object_number
                            if (section == "agreement_number") return tr.a911_contract_number
                            if (section == "hub_id") return "Hub ID"
                            if (section == "name") return tr.a911_title
                            if (section == "address") return tr.address
                            if (section == "phone_number") return tr.phone
                            if (section == "responsible_person_name") return tr.name_of_responsible
                            if (section == "responsible_person_phone_number") return tr.phone_number_of_responsible
                            return tr.na
                        }
                    }
                }

                delegate: Rectangle {
                    width: parent.width
                    height: 49
                    color: ui.colors.dark1

                    Custom.HandMouseArea {
                        onClicked: {
                            function action(tempId) {
                                searchedModel.reload_objects_model(index)

                                var tempIndex = searchedModel.get_section_index(index)
                                function inner() {
                                    objectsStack.startLoading()
                                    if (appCompany.current_facility && tempIndex == objectsStack.currentObjectIndex) {
                                        objectsStack.currentObjectIndex = -2
                                    }
                                    app.facility_module.get_facility(tempId, tempIndex)
                                }

                                return inner
                            }

                            popup.todo = action(object.id)
                            popup.close()
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.black
                        anchors.bottom: parent.bottom
                    }

                    RowLayout {
                        width: parent.width - 48
                        height: 48
                        spacing: 0
                        anchors.horizontalCenter: parent.horizontalCenter

                        Item {
                            clip: true
                            Layout.fillHeight: true
                            Layout.minimumWidth: 104
                            Layout.maximumWidth: 104

                            Custom.FontText {
                                text: number ? number : ui.empty
                                width: parent.width
                                color: ui.colors.light3
                                font.pixelSize: 14
                                maximumLineCount: 1
                                wrapMode: Text.Wrap
                                elide: Text.ElideRight
                                textFormat: Text.PlainText
                                verticalAlignment: Text.AlignVCenter
                                anchors {
                                    left: parent.left
                                    verticalCenter: parent.verticalCenter
                                }
                            }
                        }

                        TableDivider { isHeader: false }

                        Item {
                            clip: true
                            Layout.fillHeight: true
                            Layout.minimumWidth: 136
                            Layout.maximumWidth: 136

                            Custom.FontText {
                                text: name ? name : ui.empty
                                color: ui.colors.light1
                                font.pixelSize: 16
                                width: parent.width
                                maximumLineCount: 2
                                wrapMode: Text.Wrap
                                elide: Text.ElideRight
                                textFormat: Text.PlainText
                                verticalAlignment: Text.AlignVCenter
                                anchors {
                                    left: parent.left
                                    verticalCenter: parent.verticalCenter
                                }
                            }
                        }

                        TableDivider { isHeader: false }

                        Item {
                            clip: true
                            Layout.fillHeight: true
                            Layout.fillWidth: true

                            Custom.FontText {
                                text: address ? address : ui.empty
                                color: ui.colors.middle1
                                font.pixelSize: 14
                                width: parent.width - 12
                                maximumLineCount: 2
                                wrapMode: Text.Wrap
                                elide: Text.ElideRight
                                textFormat: Text.PlainText
                                verticalAlignment: Text.AlignVCenter
                                anchors {
                                    left: parent.left
                                    verticalCenter: parent.verticalCenter
                                }
                            }
                        }

                        TableDivider { isHeader: false }

                        Item {
                            clip: true
                            Layout.fillHeight: true
                            Layout.minimumWidth: 104
                            Layout.maximumWidth: 104

                            Custom.FontText {
                                text: hub_id ? hub_id : ui.empty
                                color: ui.colors.middle1
                                font.pixelSize: 14
                                width: parent.width - 12
                                maximumLineCount: 2
                                wrapMode: Text.Wrap
                                elide: Text.ElideRight
                                textFormat: Text.PlainText
                                verticalAlignment: Text.AlignVCenter
                                anchors {
                                    left: parent.left
                                    verticalCenter: parent.verticalCenter
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Component.onDestruction: {
        app.facility_module.search_facilities("")
        if (popup.todo) popup.todo()
    }
}
