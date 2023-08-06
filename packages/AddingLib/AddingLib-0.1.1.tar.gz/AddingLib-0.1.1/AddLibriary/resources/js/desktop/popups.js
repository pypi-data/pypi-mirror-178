
var exit_popup_instance = null;
var malf_popup_instance = null;
var text_popup_instance = null;
var error_popup_instance = null;
var agreement_popup_instance = null;
var delete_account_verification_popup_instance = null;

function popupByPath(path, properties={}) {
    var component = Qt.createComponent(path);
    var err = component.errorString();
    if (err) console.log(err);
    var popup = component.createObject(application, properties);
    popup.open();
    return popup
}

function waitPopup(waitSignal, waitCallback=undefined, options=undefined) {
    var component = Qt.createComponent("qrc:/resources/qml/components/911/DS3/popups/WaitPopup.qml")
    var popup = component.createObject(application, Object.assign({
        waitSignal: waitSignal, waitCallback: waitCallback
    }, options))
    popup.open()
}

function add_hub_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/hubs/popups/AddHubPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function please_wait_popup(description = tr.request_send, timeout = 30, endSignals = undefined) {
    var component = Qt.createComponent("qrc:/resources/qml/components/911/DS3/popups/StatusPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {description: description, timeout: timeout, endSignals: endSignals})
    popup.open()
    return popup
}

function please_wait_invite_users_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/PleaseWaitInviteUserPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function text_popup(title, information) {
    if (text_popup_instance != null) return
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml")
    var err = component.errorString()
    if (err) console.log(err)
    text_popup_instance = component.createObject(application, {
        title: title,
        text: information,
    })
    text_popup_instance.onClosed.connect(function() { text_popup_instance = null })
    text_popup_instance.open()
}

function error_popup(error) {
    if (error_popup_instance != null) return
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/911/DS3/popups/ModalInfo.qml")
    var err = component.errorString()
    if (err) console.log(err)
    error_popup_instance = component.createObject(application, {
        sections: [{ "description": error }],
    })
    error_popup_instance.onClosed.connect(function() { error_popup_instance = null })
    error_popup_instance.open()
}


function hub_settings_popup(device) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/hub/devices/settings/HubSettings.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"device": device})
    popup.open()
}

function add_room_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/AddRoomPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function room_settings_popup(room) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/RoomSettingsPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"room": room})
    popup.open()
}

function room_delete_popup(room) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/DeleteRoomPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"room": room})
    popup.open()
}

function hub_delete_popup(hub) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/DeleteHubPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function change_hub_name_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/ChangeHubNamePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function app_restart_required_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/AppRestartRequiredPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function invite_popup(title) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/InvitePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application,
            {"title": title})
    popup.open()
}

function select_wifi_popup_advanced() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wifi/SelectWifiNetworkAdvancedPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function add_group_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/AddGroupPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function group_settings_popup(group) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/GroupSettingsPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"group": group})
    popup.open()
}

function group_delete_popup(room) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/DeleteGroupPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"group": group})
    popup.open()
}

function select_devices_popup(group) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/SelectDevicesPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"group": group})
    popup.open()
}

function select_group_popup(devices) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/groups/SelectGroupPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"devices": devices})
    popup.open()
}

function request_access_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/RequestAccessPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function add_device_popup(hub, roomIndex) {
    var component = Qt.createComponent("qrc:/resources/qml/screens/home/pages/objects/object/popups/AddDevicePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"hub": hub, "roomIndex": roomIndex})
    popup.open()
}

function select_add_device_popup(roomIndex, management=null, from_devices=true) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/SelectAddDevicePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"roomIndex": roomIndex, "management": management, "from_devices": from_devices})
    popup.open()
}

function device_settings_popup(device, openCompanies=false) {
    var component = Qt.createComponent(device.settings_popup)
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"device": device, "openCompanies": openCompanies})
    popup.open()
}

function vhf_output_settings_popup(device, output_number) {
    var component = Qt.createComponent(device.output_settings_popup)
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"device": device, "output_number": output_number})
    popup.open()
}

function delete_device_popup(hub_id, device, management) {
    var component = Qt.createComponent("qrc:resources/qml/screens/home/pages/objects/object/managements/settings/DeleteDevicePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"hub_id": hub_id, "device": device, "management": management})
    popup.open()
}

function interconnect_popup(fire_alarms, management=null, isCriticalCOAlarm=null) {
    var component = Qt.createComponent("qrc:/resources/qml/screens/pro/pages/hubs/hub/popups/StopInterconnectPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {
            "fire_alarms": fire_alarms,
            "management": management,
            "isCriticalCOAlarm": isCriticalCOAlarm,
        })
    popup.open()
    return popup
}

function malfunctions_popup(data, incident=null) {
    if (malf_popup_instance != null) return
    var component = Qt.createComponent("qrc:/resources/qml/screens/home/pages/objects/object/popups/MalfunctionsPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    malf_popup_instance = component.createObject(
        application, {"malfunctions_data": data, "incident": incident}
    )
    malf_popup_instance.onClosed.connect(function() { malf_popup_instance = null })
    malf_popup_instance.open()
    return malf_popup_instance
}

function map_popup(information, mode) {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/AjaxMapPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"information": information, "mode": mode})
    popup.open()
    return popup
}

function whats_new(data) {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/AjaxWhatsNewPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"information": data})
    popup.open()
    return popup
}

function user_popup() {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/AjaxUserPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
    return popup
}

function application_settings_popup() {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/AjaxAppPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
    return popup
}

function report_problem() {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/AjaxProblemPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
    return popup
}

function exit_popup() {
    if (exit_popup_instance) return
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/AjaxExitPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    exit_popup_instance = component.createObject(application)
    exit_popup_instance.onClosed.connect(function(){exit_popup_instance = null})
    exit_popup_instance.open()
}

function user_settings_popup() {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/AjaxUserSettingsPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
    return popup
}

function change_user_name_popup(nameField, currentName) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/AjaxChangeUserNamePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"nameField": nameField, "currentName": currentName})
    popup.open()
}

function add_camera_popup(roomIndex, rooms) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/AddCameraPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"roomIndex": roomIndex, "rooms": rooms})
    popup.open()
}

function change_user_email_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/AjaxChangeUserEmailPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function enter_codes(data) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/AjaxEnterCodesPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"data": data})
    popup.open()
}

function change_user_password_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/AjaxChangeUserPasswordPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function change_user_phone_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/AjaxChangeUserPhonePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function image_popup(target, url, isRounded) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/ChangeImagePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"target": target, "url": url, "isRounded": isRounded})
    popup.open()
}

function motion_cam_popup(data) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/AjaxMotionCamPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"data": data})
    popup.open()
}

function add_wire_input_popup(roomIndex, management=null) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/AddWireInputPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"roomIndex": roomIndex, "management": management})
    popup.open()
}

function add_wire_siren_popup(roomIndex, management=null) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/AddWireSirenPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"roomIndex": roomIndex, "management": management})
    popup.open()
}

function add_yavir_access_control_popup(roomIndex, management=null) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/AddYavirAccessControlPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"roomIndex": roomIndex, "management": management})
    popup.open()
}

function key_reg_time_popup(hub_id, text, management=null) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/KeyRegTimePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"hub_id": hub_id, "text": text, "management": management})
    popup.open()
}

function user_key_reg_time_popup(text) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/UserKeyRegTimePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"text": text})
    popup.open()
}

function confirm_invites_popup(text, pro, emails, management=null) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/AjaxConfirmInvitesPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"text": text, "pro": pro, "emails": emails, "management": management})
    popup.open()
}

function update_popup(info) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/AjaxUpdatePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"info": info})
    popup.open()
}

function please_wait_download_popup() {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/AjaxPleaseWaitDownloadPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function open_address_map() {
    var component = Qt.createComponent(
        "qrc:/resources/qml/screens/hub/devices/settings/address/MapPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
    return popup
}

function agreement_popup(url) {
    if (agreement_popup_instance) return
    var component = Qt.createComponent(
        "qrc:/resources/qml/components/desktop/AjaxAgreementPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    agreement_popup_instance = component.createObject(application, {"url": url})
    agreement_popup_instance.onClosed.connect(function(){agreement_popup_instance = null})
    agreement_popup_instance.open()
}

function video_surveillance_settings() {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/ezviz/VideoSurveillancePopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
    return popup
}

function ezviz_login_popup() {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/ezviz/CloudLoginPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
    return popup
}

function ezviz_popup() {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/ezviz/UserPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
    return popup
}

function add_ezviz_camera_popup() {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/ezviz/AddCameraPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
    return popup
}

function add_common_camera_popup(roomIndex, rooms) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/AddCommonCameraPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"roomIndex": roomIndex, "rooms": rooms})
    popup.open()
}

function add_hikvision_safire_camera_popup(roomIndex, camType, data) {
    var component = Qt.createComponent("qrc:/resources/qml/screens/home/pages/objects/object/popups/AddHikvisionSafireCameraPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"roomIndex": roomIndex, "camType": camType, "info": data.data})
    popup.open()
}

function choose_hikvision_safire_camera_popup(data) {
    var component = Qt.createComponent("qrc:/resources/qml/screens/home/pages/objects/object/popups/ChooseHikvisionCameraPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"info": data})
    popup.open()
}


function arm_disarm_hub_settings_popup(scenario, device) {
    var component = Qt.createComponent(
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/hub_scenarios/ArmDisarmScheduleSettingsPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"scenario": scenario, "device": device})
    popup.open()
    return popup
}


function enable_interconnect_warning_popup(frame_length) {
    var component = Qt.createComponent(
        "qrc:/resources/qml/components/desktop/AjaxFireInterconnectWarningPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"frame_length": frame_length})
    popup.open()
    return popup
}

function timezones_warning_popup(todo) {
    var component = Qt.createComponent("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject
        (
            application,
            {
                title: tr.hub_time_zone_is_not_set_title,
                text: tr.hub_time_zone_is_not_set_text,
                firstButtonText: tr.continue_,
                secondButtonText: tr.cancel,
                firstButtonCallback: todo
            }
        )
    popup.open()
    return popup
}

function confirm_or_cancel(headerText, confirmText, todo, actionText=null) {
    var component = Qt.createComponent(
        "qrc:/resources/qml/components/desktop/AjaxConfirmOrCancelPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"headerText": headerText, "confirmText": confirmText, "todo": todo, "actionText": actionText})
    popup.open()
    return popup
}

function not_pd_compliant_devices_popup(not_pd_devices) {
    var component = Qt. createComponent("qrc:/resources/qml/components/desktop/NotPDCompliantDevicesPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, { "not_pd_devices" : not_pd_devices })
    popup.open()
    return popup
}

function confirm_clear_notofications(confrimText, callback) {
    var component = Qt.createComponent(
        "qrc:/resources/qml/components/desktop/AjaxDeleteNotificationsPopup.qml");
    var err = component.errorString();
    if (err) console.log(err);
    var popup = component.createObject(application, {"confirmText": confrimText, "callback": callback});
    popup.open();
    return popup;
}

function wizard_action_popup(headerLabel, content, saveText, todo) {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/WizardActionPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(
        application,
        {
            "headerLabel" : headerLabel,
            "contentText": content,
            "saveContent": saveText,
            "todo": todo
        }
    )
    popup.open()
    return popup
}

function interconnect_delay_popup(fire_alarms, trigger, management=null) {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/InterconnectDelayPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(
        application,
        {
            "fire_alarms": fire_alarms,
            "trigger": trigger,
            "management": management
        }
    )
    popup.open()
    return popup
}

function reset_alarm_popup(hub, management=null) {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/ResetAlarmPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"hub": hub, "management": management})
    popup.open()
    return popup
}

function chimes_activation_popup() {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/AjaxChimesPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}

function reset_power_for_fire_devices(todo, devices, management=null) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/components/desktop/AjaxFireAlarmsDetected.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"todo": todo, "mtr_devices": devices, "management": management})
    popup.open()
    return popup
}

function confirm_action_popup(contentText, todo, settings = {}) {
    var component = Qt.createComponent(
        "qrc:/resources/qml/components/desktop/AjaxConfirmAction.qml");
    var err = component.errorString();
    if (err) console.log(err);
    var popup = component.createObject(
        application,
        {
            "contentText": contentText,
            "todo": todo,
            "labelText": settings.labelText,
            "saveColor": settings.saveColor,
            "confirmText": settings.confirmText,
            "exitText": settings.exitText,
            "cancelTodo": settings.cancelTodo,
            "closeTodo": settings.closeTodo,
        }
    );
    popup.open();
    return popup;
}

function migration_summary_popup() {
    var component = Qt.createComponent("qrc:/resources/qml/components/desktop/MigrationSummaryPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application)
    popup.open()
}


function delete_account_verification_popup() {
    if (delete_account_verification_popup_instance != null) return
    var component = Qt.createComponent("qrc:/resources/qml/screens/home/pages/objects/object/popups/delete_account_wizard/Verification.qml")
    var err = component.errorString()
    if (err) console.log(err)
    delete_account_verification_popup_instance = component.createObject(application, {})
    delete_account_verification_popup_instance.onClosed.connect(function() { delete_account_verification_popup_instance = null })
    delete_account_verification_popup_instance.open()
}
