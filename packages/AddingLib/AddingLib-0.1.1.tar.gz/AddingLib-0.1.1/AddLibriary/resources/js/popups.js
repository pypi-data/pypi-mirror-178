
var exit_popup_instance = null;
var text_popup_instance = null;
var update_popup_instance = null;

function add_access_card_popup(mode) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/AddAccessCardPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"mode": mode})
    popup.open()
}

function add_access_card_flow_popup(hub, type, color, user_id) {
    var component = Qt.createComponent(
            "qrc:/resources/qml/screens/home/pages/objects/object/popups/AddAccessCardFlowPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    var popup = component.createObject(application, {"hub": hub, "type": type, "color": color, "user_id": user_id})
    popup.open()
}

function create_popup(name, properties={}) {
    var path = "qrc:/resources/qml/screens/popups/".concat("", name);
    var component = Qt.createComponent(path);
    var err = component.errorString();
    if (err) console.log(err);
    var popup = component.createObject(application, properties);
    popup.open();
    return popup
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

function exit_popup(action) {
    if (exit_popup_instance) return
    var component = Qt.createComponent("qrc:/resources/qml/screens/popups/ExitPopup.qml")
    var err = component.errorString()
    if (err) console.log(err)
    exit_popup_instance = component.createObject(application, {"action": action})
    exit_popup_instance.onClosed.connect(function(){exit_popup_instance = null})
    exit_popup_instance.open()
}

function create_notification(properties={}, incubate=true) {
    var path = "qrc:/resources/qml/components/911/Notification.qml";
    var component = Qt.createComponent(path);
    var err = component.errorString();
    if (err) console.log(err);

    if (incubate) {
        return component.incubateObject(application, properties);
    } else {
        return component.createObject(application, properties);
    }
}

function scheme_image_popup(gridView, incidentPage) {
    return create_popup("SchemeImagePopup.qml", {"grid": gridView, "incidentPage": incidentPage});
}

function wait_popup() {
    return create_popup("WaitPopup.qml");
}

function add_employee_popup() {
    return create_popup("AddEmployeePopup2.qml");
}

function add_fast_response_team_popup() {
    return create_popup("AddFastResponseTeamPopup.qml");
}

function user_popup() {
    return create_popup("UserPopup.qml");
}

function calendar_popup(action, selectedDate, allowFuture, allowPast=true, additionalParams=null) {
    var data = {"action": action, "selectedDate": selectedDate, "allowFuture": allowFuture, "allowPast": allowPast}
    if (additionalParams) {
        data = Object.assign({}, data, additionalParams)
    }
    return create_popup("CalendarPopup.qml", data);
}

function sign_up_popup(step=0, email="", phoneNumber="") {
    return create_popup("SignUpPopup.qml", {"stepAlt": step, "userEmail": email, "phoneNumber": phoneNumber});
}

function add_responsible_person_popup() {
    return create_popup("AddResponsiblePersonPopup.qml");
}

function confirmation_deletion_popup(task, text=null) {
    return create_popup("ConfirmationDeletionPopup.qml", {"task": task, "popup_text": text});
}

function easter_egg_popup() {
    return create_popup("EasterEggPopup.qml");
}

function motion_cam_popup(grid, incidentPage) {
    return create_popup("MotionCamPopup.qml", {"grid": grid, "incidentPage": incidentPage});
}

function facility_motion_cam_popup(event) {
    return create_popup(
        event.event.hub_event.source_type == "0D" ? "FacilityMotionCamPopup.qml" : "FacilityMotionCamOutdoorPopup.qml",
        {"event": event}
    );
}

function upload_facility_media() {
    return create_popup("UploadFacilityMediaPopup.qml");
}

function delete_facility_media(media) {
    return create_popup("DeleteFacilityMediaPopup.qml", {"media": media});
}

function update_facility_media(media) {
    return create_popup("UpdateFacilityMediaPopup.qml", {"media": media});
}

function to_sleep_mode_popup(facility_id) {
    return create_popup("ToSleepModePopup.qml", {"facilityId": facility_id});
}

function add_facility_note() {
    return create_popup("AddFacilityNotePopup.qml");
}

function add_object_popup(connectionsAdd=false, hub_id="", name="", number="", hub_company_binding_state=null) {
    return create_popup("AddObjectPopup.qml", {
        "connectionsAdd": connectionsAdd,
        "hubId": hub_id,
        "name": name,
        "number": number,
        "hubCompanyBindingState": hub_company_binding_state
    });
}

function schedule_menu_popup(parent) {
    return create_popup("ScheduleMenuPopup.qml", {"parent": parent});
}

function schedule_time_popup(parent, updateBody) {
    return create_popup("ScheduleTimePopup.qml", {"parent": parent, "updateBody": updateBody});
}

function password_change_popup(email="") {
    return create_popup("PasswordChangePopup.qml", {"email": email});
}

function user_settings_popup() {
    return create_popup("UserSettingsPopup.qml");
}

function user_changed_password_popup() {
    return create_popup("user_settings/PasswordChangedPopup.qml");
}

function maps_popup(info) {
    return create_popup("MapsPopup.qml", {"info": info});
}

function remove_facility(facility, mode="facility") {
    return create_popup("RemoveImmediately.qml", {"facility": facility, "mode": mode});
}

function confirm_change_password(title, additionalTitle) {
    return create_popup("ConfirmChangePasswordSettingUser.qml", {'title': title, "additionalTitle": additionalTitle});
}

function notification_popup(text) {
    return create_popup("NotificationPopup.qml", {"text": text});
}

function edit_phone_number_popup() {
        return create_popup("EditPhoneNumberPopup.qml");
}

function edit_email_popup(email) {
        return create_popup("EditEmailPopup.qml", {"email": email});
}

function confirmation_common_popup(todo, text, buttonText=null, buttonColor=null) {
    var additional = {"todo": todo, "text": text}
    if (buttonText) additional["buttonText"] = buttonText
    if (buttonColor) additional["buttonColor"] = buttonColor
    return create_popup("ConfirmCommonPopup.qml", additional);
}

function facilities_search_popup(objectsStack) {
    return create_popup("FacilitiesSearchPopup.qml", {"objectsStack": objectsStack});
}

function incidents_logs(activities, parent, x, y, iconY) {
    return create_popup(
    "IncidentsLogsPopup.qml",
     {"activities": activities,
      "parent": parent,
       "x1": x - 344, "y1": y, "iconY": iconY});
}

function report_popup(data) {
    return create_popup("ReportPopup.qml", data);
}

function update_popup(update_data) {
    if (update_popup_instance) update_popup_instance.destroy()
    var path = "qrc:/resources/qml/UpdatePopup.qml";
    var component = Qt.createComponent(path);
    var err = component.errorString();
    if (err) console.log(err);
    update_popup_instance = component.createObject(application, {"update_data": update_data});
    update_popup_instance.open();
    update_popup_instance.onClosed.connect(function() { update_popup_instance = null })
    return update_popup_instance
}

function time_sync_popup() {
    return create_popup("TimeSyncPopup.qml");
}


function connections_filter_popup(filters, counters, total_counter) {
    return create_popup("ConnectionsFilterPopup.qml", {
        "counters":counters,
        "filters": filters,
        "total_counter": total_counter
    });
}

function delete_translator_facility_popup(text, remove) {
    return create_popup("DeleteTranslatorFacilityPopup.qml", {
        "text": text,
        "remove": remove});
}

function create_911_channel_popup(settings, mode="facility") {
    // temporary
    return create_popup("Create911ChannelPopup.qml", {"settings": settings, "mode": mode});
}

function remove_911_channel_popup(settings) {
    // temporary
    return create_popup("Remove911ChannelPopup.qml", {"settings": settings});
}

function delete_hub_company_binding(settings, mode="facility") {
    // temporary
    return create_popup("DeleteHubCompanyBindingPopup.qml", {"settings": settings, "mode": mode});
}

function delete_installer(settings, reloadSignal, mode, insertData) {
    // temporary
    return create_popup("DeleteInstallerPopup.qml", {"settings": settings, "reloadSignal": reloadSignal, "mode": mode, "insertData": insertData});
}

function add_alt_object_popup(mode="facility") {
    // temporary
    return create_popup("AddAltObjectPopup.qml", {"mode": mode});
}

function plan_full_screen_popup(url) {
    return create_popup("PlanFullScreenPopup.qml", {"url": url});
}

function create_workplace_popup(workplace, incident_id=null) {
    return create_popup("CreateWorkplacePopup.qml", {"workplace": workplace, "incident_id": incident_id});
}

function facility_versioning_popup(text, continue_saving) {
    return create_popup("FacilityVersioningPopup.qml", {"text": text, "continue_saving": continue_saving});
}

function bindings_filter_popup() {
    return create_popup("BindingsFilterPopup.qml");
}

function company_incident_settings_popup() {
    return create_popup("CompanyIncidentSettingsPopup.qml");
}

function hubs_availability_popup(result) {
    return create_popup("HubsAvailabilityPopup.qml", {"result": result});
}

function installer_access_popup(parent, facility_id, employee_id, mode) {
    return create_popup("InstallerAccessPopup.qml", {"parent": parent, "facilityId": facility_id, "employeeId": employee_id, "mode": mode});
}

function add_installer_popup(facility) {
    return create_popup("AddInstallersPopup.qml", {"facility": facility});
}

function facilities_permissions_popup(employee) {
    return create_popup("FacilitiesPermissionsPopup.qml", {"employee": employee});
}

function add_installer_facility_popup(employee) {
    return create_popup("AddInstallersFacilityPopup.qml", {"employee": employee});
}

function add_multitransmitter_device_popup(roomIndex, device) {
    return create_popup("AddMultitransmitterDevicePopup.qml", {"roomIndex": roomIndex, "mtr_device": device});
}

function pro_access_popup(parent, hub) {
    return create_popup("ProAccessPopup.qml", {"parent": parent, "hub": hub});
}

function terminate_session_warning_popup(logoutText, todo, isTwoFa) {
    return create_popup("AjaxWarningSessionPopup.qml", {"logoutText": logoutText, "todo": todo, "isTwoFa": isTwoFa});
}

function second_step_2fa_popup() {
    return create_popup("SecondStepTwoFaPopup.qml");
}

function confirm_action_popup(contentText, todo, settings = {}) {
    return create_popup(
        "AjaxConfirmAction.qml",
        {
            "contentText": contentText,
            "todo": todo,
            "labelText": settings.labelText,
            "saveColor": settings.saveColor,
            "confirmText": settings.confirmText,
            "exitText": settings.exitText
        }
    );
}

function two_fa_activated() {
    return create_popup("TwoFaActivatedPopup.qml")
}

function two_fa_confirm_login(loginData) {
    return create_popup("AjaxTwoFaConfirmLoginPopup.qml", {"loginData": loginData})
}

function sessions_popup() {
    return create_popup("AjaxSessionsPopup.qml")
}

function confirm_entering_popup(session) {
    return create_popup("AjaxConfirmEntering.qml", {"session": session})
}

function hub_alarm_countdown_popup(action, ignoreAlarms, incidentItem=null) {
    return create_popup("AlarmCountdownTimerPopup.qml", {"action": action, "ignoreAlarms": ignoreAlarms, "incidentItem": incidentItem})
}

function dco_event_info_popup(eventCode) {
    return create_popup("DcoEventInfoPopup.qml", {"eventCode": eventCode})
}

function antimasking_sensors_failed_popup() {
    return create_popup("AntimaskingSensorFailedPopup.qml")
}

function voltage_drop_popup(device_type) {
    return create_popup("VoltageDropPopup.qml")
}

function internal_crash_popup() {
    return create_popup("InternalCrashPopup.qml")
}

function confirm_email_popup(confirmationInfo, companyStack, ownership) {
    return create_popup("ConfirmEmailPopup.qml", {"confirmationInfo": confirmationInfo, "companyStack": companyStack, "ownership": ownership})
}

function image_popup(url) {
    return create_popup("ImagePopup.qml", {"url": url})
}

function confirm_email_popup_alt(confirmationInfo, companyStack, ownership) {
    return ownership
           ? create_popup("ConfirmEmailPopup.qml", {"confirmationInfo": confirmationInfo, "companyStack": companyStack, "ownership": ownership})
           : create_popup("ConfirmEmailEditPopup.qml", {"confirmationInfo": confirmationInfo, "preset": companyStack})
}

function cancel_wizard_popup(close_wizard_action) {
    return create_popup("CancelWizardPopup.qml", {'close_wizard_action': close_wizard_action})
}