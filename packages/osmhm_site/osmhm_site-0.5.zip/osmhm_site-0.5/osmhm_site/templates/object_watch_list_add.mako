<%inherit file="base.mako"/>
<%block name="header">
</%block>
<%block name="content">
<form class="form-horizontal" method="POST">
	<fieldset>
		<legend>Add object to watch list:</legend>
		<div class="form-group">
			<label for="addusername" class="col-lg-4 control-label">Object reference</label>
			<div class="col-lg-6">
				<input type="text" class="form-control" id="addobjectname" name="addobjectname" placeholder="e.g. r100023" required>
				<span class="help-block">Prefix the reference by the type of object: node=n, way=w, relation=r. Then immediately follow this prefix with the id number (in other words, please don't add a space).
			</div>
		</div>
		<div class="form-group">
			<label for="addreason" class="col-lg-4 control-label">Reason:</label>
			<div class="col-lg-6">
				<input type="text" class="form-control" id="addreason" name="addreason" placeholder="e.g. Vandalised often" required>
				<span class="help-block">Enter a note to yourself why this object was added.</span>
			</div>
		</div>
		<div class="form-group">
			<label for="addnotify" class="col-lg-4 control-label">Notification email:</label>
			<div class="col-lg-6">
				<input type="text" class="form-control" id="addnotify" name="addnotify" placeholder="Email address (optional)">
				<span class="help-block">Add an optional notification email address.</span>
			</div>
		</div>
		<div class="form-group">
			<div class="col-lg-10 col-lg-offset-6">
				<button class="btn btn-primary" type="submit" value="submit">Submit</button>
			</div>
		</div>
	</fieldset>
</form>
</%block>
