import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    id: addressSettings

    property var sideMargin: 24
    property var lat: hub.latitude
    property var lon: hub.longitude

    Connections {
        target: app

        onGeoData: {
            addressSettings.lat = data.latitude
            addressSettings.lon = data.longitude

            coordinates.atomInput.text = data.latitude + ", " + data.longitude
            country.currentCountryCode = data.country_code
            region.atomInput.text = data.loc_state
            city.atomInput.text = data.locality
            address.atomInput.text = data.address
            comment.atomInput.text = ""
        }

        onActionSuccess: {
            changesChecker.changeInitialValues()
        }
    }

    anchors.fill: parent

    color: ui.backgrounds.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            coordinates.atomInput.text,
            comment.atomInput.text
        ]
    }

    DS3.NavBarModal {
        id: addressSettingsBar

        headerText: tr.address
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: addressSettingsBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: coordinates

                allowClickIconWhenReadOnly: true

                atomInput {
                    label: tr.coordinates
                    readOnly: true
                    required: false
                    text: [", ", "0.00000, 0.00000"].includes(hub.latitude + ", " + hub.longitude) ? "" : hub.latitude + ", " + hub.longitude
                }

                rightIcon {
                    source: "qrc:/resources/images/Athena/views_icons/Geoposition-M.svg"
                    visible: true
                }

                onRightIconClicked: {
                    var info = {"mode": "address", "info": {"lat": addressSettings.lat, "lon": addressSettings.lon}}

                    Popups.maps_popup(info)
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: country

                property var currentCountryCode: hub.country_code

                onCurrentCountryCodeChanged: {
                    atomInput.text = util.get_country_by_code(currentCountryCode, tr.get_selected())
                }

                visible: coordinates.atomInput.text.length
                atomInput {
                    label: tr.country
                    text: util.get_country_by_code(currentCountryCode, tr.get_selected())
                    readOnly: true
                    required: false
                }
            }
        }

        DS3.Spacing {
            height: country.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: region

                visible: coordinates.atomInput.text.length
                atomInput {
                    text: hub.loc_state
                    label: tr.region
                    readOnly: true
                    required: false
                }
            }
        }

        DS3.Spacing {
            height: region.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: city

                visible: coordinates.atomInput.text.length
                atomInput {
                    text: hub.locality
                    label: tr.city
                    readOnly: true
                    required: false
                }
            }
        }

        DS3.Spacing {
            height: city.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: address

                visible: coordinates.atomInput.text.length
                atomInput {
                    text: hub.address
                    label: tr.address
                    readOnly: true
                    required: false
                }
            }
        }

        DS3.Spacing {
            height: address.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: comment

                visible: coordinates.atomInput.text.length
                atomInput {
                    text: hub.address_comment
                    label: tr.additional_info
                    required: false
                }
            }
        }

        DS3.Spacing {
            height: comment.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.ButtonRow {
                id: removeAddress

                text: tr.remove_address_monitoring
                isDanger: true
                visible: coordinates.atomInput.text.length

                onClicked: {
                    coordinates.atomInput.text = ""
                    country.currentCountryCode = ""
                    region.atomInput.text = ""
                    city.atomInput.text = ""
                    address.atomInput.text = ""
                    comment.atomInput.text = ""
                }
            }
        }
    }
    DS3.ButtonBar {
        id: saveButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.save
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            var settings = {
                "hub_address": {
                    "country_code": country.currentCountryCode.toUpperCase(),
                    "loc_state": region.atomInput.text,
                    "locality": city.atomInput.text,
                    "address": address.atomInput.text,
                    "comment": comment.atomInput.text,
                    "latitude": {
                        "scale": 6,
                        "_decimal": "",
                    },
                    "longitude": {
                        "scale": 6,
                        "_decimal": "",
                    },
                },
                "_params": {
                    "skip_comparison_check": [],
                },
            }

            var coordinatesList = coordinates.atomInput.text ? util.split(coordinates.atomInput.text, ", ") : ["", ""]

            if (coordinates.atomInput.text != "") {
                settings["hub_address"]["latitude"]["_decimal"] = coordinatesList[0]
                settings["hub_address"]["longitude"]["_decimal"] = coordinatesList[1]
            }

            // changing 'unscaledBytes' only won't cause changes (server-side trouble)
            if (hub.latitude != coordinatesList[0]) {
                // different zero-representation problem ("" and "0.00000") - ignore
                if (hub.latitude + coordinatesList[0] != "0.00000") {
                    settings["_params"]["skip_comparison_check"].push("hub_address.latitude.scale")
                }
            }
            if (hub.longitude != coordinatesList[1]) {
                // different zero-representation problem ("" and "0.00000") - ignore
                if (hub.longitude + coordinatesList[1] != "0.00000") {
                    settings["_params"]["skip_comparison_check"].push("hub_address.longitude.scale")
                }
            }

            DesktopPopups.please_wait_popup()
            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}
