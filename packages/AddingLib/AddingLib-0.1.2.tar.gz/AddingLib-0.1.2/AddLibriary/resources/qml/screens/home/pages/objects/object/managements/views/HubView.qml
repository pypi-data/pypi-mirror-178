import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as Settings
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/images.js" as Images


DS3.ScrollView {
    property var device: null

    opacity: device && device.online ? 1.0 : 0.3
    padding: 24

    ViewsParts.DeviceNameRoom {}
    DS3.DeviceHeaderInfo {
        imagePath: Images.get_image(hub.image_type_name, "Large", hub.color)
    }

    DS3.SettingsContainer {
        // Malfunctions
        DS3.InfoTitleButtonIcon {
            visible: device.malfunctions.length > 0 && !device.hide_malfunctions
            atomTitle.title: tr.malfunctions
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/Warning-M.svg"
            status: ui.ds3.status.ATTENTION
            buttonIcon.source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"

            onRightControlClicked: {
                var malfText = []

                if (device.malfunctions.includes("FLASH_MALFUNCTION")) malfText.push(tr.malfunction_31)
                if (device.malfunctions.includes("SOFTWARE_MALFUNCTION")) malfText.push(tr.malfunction_30)
                if (device.malfunctions.includes("BATTERY_MALFUNCTION")) malfText.push(tr.malfunction_28)
                if (device.malfunctions.includes("BATTERY_CHARGE_ERROR")) malfText.push(tr.malfunction_29)
                if (device.malfunctions.includes("WIFI_CONNECTION_FAIL")) malfText.push(tr.malfunction_27)

                DesktopPopups.error_popup(malfText.join("\n"))
            }
        }

        // System Restore
        DS3.InfoTitleButtonMini {
            visible: hub && hub.alarm_happened
            enabled: {
                if (!appUser.company_id) return true
                if (managementInIncident && incident.status != "PROCESSING") return false
                return companyAccess.HUB_AFTER_ALARM_RESTORATION_REQUEST || companyAccess.HUB_AFTER_ALARM_RESTORE
            }
            atomTitle.title: tr.system_restore_required
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/RestoreAfterAlarm-M.svg"
            status: ui.ds3.status.ATTENTION
            buttonMini {
                source: "qrc:/resources/images/Athena/views_icons/Restore-M.svg"
                color: ui.ds3.figure.attention
            }
            onRightControlClicked: {
                DesktopPopups.reset_alarm_popup(hub, management)
            }
        }

        // Gsm Signal Level
        DS3.InfoSignal {
            visible: device.gsm_gprs_enabled
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/CellularData-M.svg"
            atomTitle.title: tr.gsm_signal_strength
            atomConnection.strength: {
                if (device.signal_strength == "NO_SIGNAL_LEVEL_INFO") { return 0 }
                return ["NO_SIGNAL", "WEAK", "NORMAL", "STRONG"].indexOf(device.gsm_signal_strength)
            }
        }

        // WiFi Signal Level
        DS3.InfoSignal {
            visible: {
                if (!hub) return false
                return ["HUB_PLUS", "HUB_2_PLUS"].includes(hub.hub_type) ? device.wifi_enabled : false
            }
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/WiFi-M.svg"
            atomTitle.title: tr.wifi_signal_strength
            atomConnection.strength: {
                if (device.signal_strength == "NO_SIGNAL_LEVEL_INFO") { return 0 }
                return ["NO_SIGNAL", "WEAK", "NORMAL", "STRONG"].indexOf(device.wifi_signal_strength)
            }
        }

        // Connection State
        DS3.InfoTitle {
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/Connection-M.svg"
            atomTitle {
                title: tr.connection_state
                subtitle: device.online ? tr.online : tr.offline
            }
        }

        // Battery Charge
        DS3.InfoTitle {
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/BatteryCharge-M.svg"
            status: device.battery_state == "MALFUNCTION" || device.battery <= 20 ?
                ui.ds3.status.ATTENTION :
                ui.ds3.status.DEFAULT
            atomTitle {
                title: tr.battery_charge
                subtitle: {
                    if (device.battery_state == "MALFUNCTION") {
                        return tr.error
                    }

                    if (device.battery_state == "CHARGING" && (["YAVIR", "YAVIR_PLUS", "HUB_FIBRA"].includes(device.hub_type))) {
                        return tr.charging
                    }

                    return device.battery == "N/A" ? tr.na : device.battery + " %"
                }
            }
        }

        // Tamper Status
        DS3.InfoTitle {
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/Lid-M.svg"
            status: device.tampered == 1 ?
                ui.ds3.status.ATTENTION :
                ui.ds3.status.DEFAULT

            atomTitle {
                title: tr.lid_state
                subtitle: {
                    if (device.tampered == "N/A") return tr.na
                    return device.tampered == "1" ? tr.opened : tr.closed
                }
            }
        }

        // Buses Power Supply
        DS3.InfoTitle {
            visible: hub.hub_type == "HUB_FIBRA"
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/Wires-M.svg"
            status: hub.bus_status.includes("SHORT_CIRCUIT_PRESENT") ?
                ui.ds3.status.ATTENTION :
                ui.ds3.status.DEFAULT
            atomTitle {
                title: tr.wires_power_state
                subtitle: {
                    if (hub.bus_status.includes("SHORT_CIRCUIT_PRESENT")) return tr.detectors_shorted_out
                    return hub.bus_status.includes("POWERED_ON") ? tr.on : tr.off
                }
            }
        }

        Settings.ExternalPower {}

        // rssi
        DS3.InfoTitle {
            visible: device.hub_type != "YAVIR"
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/AvarageNoise-M.svg"
            atomTitle {
                title: tr.average_noise
                subtitle: {
                    var noise1 = device.average_noise
                    var noise2 = device.average_noise_2

                    if (!["HUB_2", "HUB_2_4G", "YAVIR_PLUS", "HUB_2_PLUS", "HUB_FIBRA"].includes(device.hub_type)) {
                        var out = ""
                        if (noise1 == "N/A") {
                            out += tr.na + " / "
                        } else {
                            out += noise1 + " / "
                        }
                        if (noise2 == "N/A") {
                            out += tr.na
                        } else {
                            out += noise2
                        }
                        status = hub && hub.high_noise_level ?
                            ui.ds3.status.ATTENTION :
                            ui.ds3.status.DEFAULT
                        return out
                    } else {
                        var out = ""
                        var noise3 = device.average_data_channel_noise
                        if (noise1 == "N/A") {
                            out += tr.na + " / "
                        } else {
                            out += noise1 + " / "
                        }
                        if (noise2 == "N/A") {
                            out += tr.na
                        } else {
                            out += noise2
                        }

                        if (hub && (hub.firmware_version_dec >= 207102 && hub.firmware_version_dec <= 207164)) {
                            if (hub.high_noise_level) {
                                status = ui.ds3.status.ATTENTION
                            } else {
                                status = ui.ds3.status.DEFAULT
                            }
                        } else {
                            if (noise3 == "N/A") {
                                out += " / " + tr.na
                            } else {
                                out += " / " + noise3
                            }
                            if (hub && (hub.high_noise_level || hub.high_noise_level_data_channel)) {
                                status = ui.ds3.status.ATTENTION
                            } else {
                                status = ui.ds3.status.DEFAULT
                            }
                        }
                        return out
                    }
                }
            }
        }

        // Cellular
        DS3.InfoTitle {
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/CellularData-M.svg"
            status: device.gsm_gprs_enabled && !device.is_gsm_active ?
                ui.ds3.status.ATTENTION :
                ui.ds3.status.DEFAULT
            atomTitle {
                title: tr.cellular
                subtitle: {
                    if (!device.gsm_gprs_enabled) return tr.off
                    return device.is_gsm_active ? tr.connected : tr.not_connected
                }
            }
        }

        // WiFi Connection
        DS3.InfoTitle {
            visible: device.hub_type == "HUB_PLUS" || device.hub_type == "HUB_2_PLUS"
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/WiFi-M.svg"
            status: device.wifi_enabled && !device.wifi_active ?
                ui.ds3.status.ATTENTION :
                ui.ds3.status.DEFAULT
            atomTitle {
                title: "Wi-Fi"
                subtitle: {
                    if (!device.wifi_enabled) return tr.off
                    return device.wifi_active ? tr.connected : tr.not_connected
                }
            }
        }

        // Sim 1
        DS3.InfoTitleButtonIcon {
            visible: device.gsm_gprs_enabled
            atomTitle {
                title: device.active_sim == 0 ?
                    "SIM1 (" + tr.active + ")" :
                    "SIM1"
                subtitle: hub && hub.sim_card_1_number ? "+" + hub.sim_card_1_number : tr.unknown_number
            }
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/Sim-M.svg"
            buttonIcon {
                source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"
                visible: ![tr.unknown_number, "+ "].includes(atomTitle.subtitle)
            }
        }

        // Sim 2
        DS3.InfoTitleButtonIcon {
            visible: hub && hub.hub_type != "HUB" && device.gsm_gprs_enabled
            atomTitle {
                title: device.active_sim == 1 ?
                    "SIM2 (" + tr.active + ")" :
                    "SIM2"
                subtitle: hub && hub.sim_card_2_number ? "+" + hub.sim_card_2_number : tr.unknown_number
            }
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/Sim-M.svg"
            buttonIcon {
                source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"
                visible: ![tr.unknown_number, "+ "].includes(atomTitle.subtitle)
            }
        }

        // Ethernet Connection
        DS3.InfoTitleButtonIcon {
            property bool isBad: !device.eth_active && device.eth_enabled

            atomTitle {
                title: tr.log_types_1
                titleColor: ui.ds3.figure.secondary
                subtitle: {
                    if (device.eth_active) return tr.connected
                    return device.eth_enabled ? tr.not_connected : tr.off
                }
            }
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/Ethernet-M.svg"
            status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
            buttonIcon.source: "qrc:/resources/images/Athena/views_icons/Info-M.svg"
            buttonIcon.visible: device.eth_active || device.eth_enabled

            onRightControlClicked: {
                DesktopPopups.popupByPath(
                    "qrc:/resources/qml/screens/home/pages/objects/object/popups/EthConnectionDetails.qml", {
                        "device": device
                    }
                )
            }
        }

        // Monitoring
        DS3.InfoTitle {
            visible: device.eth_cms_enabled || device.gprs_cms_enabled || device.cms_wifi_enabled
            leftIcon.source: "qrc:/resources/images/Athena/views_icons/Monitoring-M.svg"
            status: device.cms_active == "N/A" ||
                !(device.eth_cms_active || device.gsm_cms_active || device.wifi_cms_active) ?
                ui.ds3.status.ATTENTION :
                ui.ds3.status.DEFAULT
            atomTitle {
                title: tr.monitoring_station
                subtitle: {
                    if (device.cms_active == "N/A") return tr.na
                    return device.eth_cms_active || device.gsm_cms_active || device.wifi_cms_active ?
                        tr.connected :
                        tr.not_connected
                }
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    ViewsParts.HubFooter {}
}