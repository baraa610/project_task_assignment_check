# Installation Guide for Task Assignment Monitor

## Quick Start Guide

This guide will help you install and configure the Task Assignment Monitor module in Odoo 17.

## Option 1: Installation on Existing Odoo 17 Server

### Step 1: Prerequisites
Ensure you have Odoo 17 installed with these modules:
- Project Management (`project`)
- Time Off (`hr_holidays`)
- Discuss (`mail`)

### Step 2: Deploy the Module

1. Copy the `task_assignment_monitor` folder to your Odoo addons directory:
   ```bash
   sudo cp -r task_assignment_monitor /path/to/odoo/addons/
   ```

2. Set proper permissions:
   ```bash
   sudo chown -R odoo:odoo /path/to/odoo/addons/task_assignment_monitor
   ```

3. Restart Odoo:
   ```bash
   sudo systemctl restart odoo
   ```

### Step 3: Install via Odoo Interface

1. Log in to Odoo as administrator
2. Go to **Apps** menu
3. Click **Update Apps List** (⟳ icon)
4. Remove the "Apps" filter to see all modules
5. Search for "Task Assignment Monitor"
6. Click **Install**

### Step 4: Verify Installation

1. Go to **Project** menu
2. You should see a new menu item: **Uncovered Tasks**
3. Create a test task and assign it to a user on leave
4. An alert should appear on the task form

## Option 2: Installation via Docker

If you want to test in a Docker environment:

```bash
# Create docker-compose.yml with Odoo 17
docker-compose up -d

# Copy module to container
docker cp task_assignment_monitor odoo_container:/mnt/extra-addons/

# Restart container
docker restart odoo_container

# Install via command line
docker exec -it odoo_container odoo -d database_name -i task_assignment_monitor --stop-after-init
```

## Option 3: Development/Testing Setup

For development or testing on Replit or local machine:

### Requirements:
- Python 3.10+
- PostgreSQL 12+
- Odoo 17 source code

### Steps:

1. **Install PostgreSQL** (if not already installed):
   ```bash
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   ```

2. **Create Database**:
   ```bash
   sudo -u postgres createuser -s odoo
   sudo -u postgres createdb odoo_test
   ```

3. **Install Odoo 17**:
   ```bash
   git clone https://github.com/odoo/odoo.git --depth 1 --branch 17.0
   cd odoo
   pip install -r requirements.txt
   ```

4. **Configure Odoo**:
   - Update `odoo.conf` with your paths
   - Set `addons_path` to include the module directory

5. **Run Odoo**:
   ```bash
   ./odoo-bin -c odoo.conf -d odoo_test -i task_assignment_monitor
   ```

6. **Access Odoo**:
   - Open browser: `http://localhost:8069`
   - Create admin account
   - Install required modules (Project, HR Leave)

## Post-Installation Configuration

### 1. Set Up Users and Employees

1. Go to **Settings → Users & Companies → Users**
2. Ensure users have linked employee records
3. Go to **HR → Employees** to verify

### 2. Configure Leave Types

1. Go to **Time Off → Configuration → Time Off Types**
2. Ensure you have at least one leave type configured
3. Create some test leave requests and approve them

### 3. Create Test Projects and Tasks

1. Go to **Project → Create**
2. Add project manager
3. Create tasks and assign to team members
4. Try assigning to someone on leave to test alerts

### 4. Configure Notifications (Optional)

1. Go to **Settings → Technical → Email Templates**
2. Find "Uncovered Task Alert" template
3. Customize subject/body as needed
4. Configure outgoing email server in Settings

## Customization

### Change Busy Threshold

Edit `models/project_task.py` and modify:
```python
elif active_tasks_count >= 3:  # Change 3 to your threshold
```

Then upgrade the module:
```bash
./odoo-bin -c odoo.conf -d database_name -u task_assignment_monitor
```

### Add Custom Alert Criteria

You can extend the availability check in `_compute_assignee_availability` method to add:
- Skills mismatch
- Department conflicts
- Time zone considerations
- Custom business rules

## Troubleshooting

### Module Not Appearing in Apps List
- Ensure folder name is exactly `task_assignment_monitor`
- Check odoo.conf has correct `addons_path`
- Verify file permissions
- Update apps list (F5 might not work, use Update button)

### Alerts Not Creating
- Verify HR Leave module is installed
- Check that leave requests are in "Approved" status
- Ensure users have linked employee records
- Check Odoo logs for errors

### Permissions Issues
- Go to **Settings → Users & Companies → Groups**
- Ensure users have "User: All Documents" for Project Management
- Check access rights in **Settings → Technical → Security → Access Rights**

### Email Not Sending
- Configure outgoing mail server in **Settings → Technical → Outgoing Mail Servers**
- Test email sending
- Check Odoo logs for SMTP errors

## Upgrading the Module

After making code changes:

```bash
# Command line upgrade
./odoo-bin -c odoo.conf -d database_name -u task_assignment_monitor

# Or via interface:
# Apps → Task Assignment Monitor → Upgrade
```

## Uninstallation

1. Go to **Apps**
2. Search "Task Assignment Monitor"
3. Click **Uninstall**
4. Confirm - this will remove all module data

## Support Resources

- Odoo Documentation: https://www.odoo.com/documentation/17.0/
- Odoo Forum: https://www.odoo.com/forum
- Check logs: `/var/log/odoo/odoo.log`

---

**Ready to Use!** Once installed, the module will automatically start monitoring task assignments.
