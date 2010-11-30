<%inherit file="/base.mako"/>
<%namespace file="/message.mako" import="render_msg" />

<script type="text/javascript">
    $( document ).ready( function () {
        $( '.role_add_button' ).click( function() {
            var action = this.id.substring( 0, this.id.lastIndexOf( '_add_button' ) )
            var in_select = '#' + action + '_in_select';
            var out_select = '#' + action + '_out_select';
            return !$( out_select + ' option:selected' ).remove().appendTo( in_select );
        });
        $( '.role_remove_button' ).click( function() {
            var action = this.id.substring( 0, this.id.lastIndexOf( '_remove_button' ) )
            var in_select = '#' + action + '_in_select';
            var out_select = '#' + action + '_out_select';
            return !$( in_select + ' option:selected' ).remove().appendTo( out_select );
        });
        $( 'form#request_type_permissions' ).submit( function() {
            $( '.in_select option' ).each(function( i ) {
                $( this ).attr( "selected", "selected" );
            });
        });
    });
</script>

<br/><br/>
<ul class="manage-table-actions">
    <li><a class="action-button" id="request_type-${request_type.id}-popup" class="menubutton">Configuration Actions</a></li>
    <div popupmenu="request_type-${request_type.id}-popup">
        <li><a class="action-button" href="${h.url_for( controller='sequencer', action='view_request_type', id=trans.security.encode_id( request_type.id ) )}">Browse configuration</a></li>
        <li><a class="action-button" href="${h.url_for( controller='sequencer', action='edit_request_type', id=trans.security.encode_id( request_type.id ) )}">Edit configuration</a></li>
        <li><a class="action-button" href="${h.url_for( controller='sequencer', action='delete_request_type', id=trans.security.encode_id( request_type.id ) )}">Delete configuration</a></li>
    </div>
</ul>

%if message:
    ${render_msg( message, status )}
%endif

<div class="toolForm">
    <div class="toolFormTitle">Manage access permissions on sequencer interface "${request_type.name}"</div>
    <div class="toolFormBody">
        <form name="request_type_permissions" id="request_type_permissions" action="${h.url_for( controller='sequencer', action='request_type_permissions', id=trans.security.encode_id( request_type.id ) )}" method="post">
            <div class="form-row">
                <%
                    current_actions = request_type.actions
                    action = trans.app.security_agent.permitted_actions.REQUEST_TYPE_ACCESS
                    all_roles = roles
                    action_key = 'REQUEST_TYPE_ACCESS'
                    
                    import sets
                    in_roles = sets.Set()
                    for a in current_actions:
                        if a.action == action.action:
                            in_roles.add( a.role )
                    out_roles = filter( lambda x: x not in in_roles, all_roles )
                %>
                ${action.description}<br/><br/>
                <div style="width: 100%; white-space: nowrap;">
                    <div style="float: left; width: 50%;">
                        Roles associated:<br/>
                        <select name="${action_key}_in" id="${action_key}_in_select" class="in_select" style="max-width: 98%; width: 98%; height: 150px; font-size: 100%;" multiple>
                            %for role in in_roles:
                                <option value="${role.id}">${role.name}</option>
                            %endfor
                        </select> <br/>
                        <div style="width: 98%; text-align: right"><input type="submit" id="${action_key}_remove_button" class="role_remove_button" value=">>"/></div>
                    </div>
                    <div style="width: 50%;">
                        Roles not associated:<br/>
                        <select name="${action_key}_out" id="${action_key}_out_select" style="max-width: 98%; width: 98%; height: 150px; font-size: 100%;" multiple>
                            %for role in out_roles:
                                <option value="${role.id}">${role.name}</option>
                            %endfor
                        </select> <br/>
                        <input type="submit" id="${action_key}_add_button" class="role_add_button" value="<<"/>
                    </div>
                </div>
            </div>
            <div class="form-row">
                <input type="submit" name="update_roles_button" value="Save"/>
            </div>
        </form>
    </div>
</div>