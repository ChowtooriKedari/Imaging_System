% Mohammad Asif Zaman
% Hesselink research group
% Part of iLabs 
% Sept-Oct 2020
% Code for initializing motor for Thorlabs TDC001 controller
% for Thorlabs MTS25-Z8 stage

function yout = TDC001(serial_num, timeout_val)

% Install Kinesis before running the code
% (https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10285)

%Example for programming the Thorlabs TDC001 with Kinesis in MATLAB, with PRM1-Z8 stage.

%Load assemblies
%Point to appropriate directory/folder if the driver is installed on a
%different location

NET.addAssembly('C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.DeviceManagerCLI.dll');
NET.addAssembly('C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.GenericMotorCLI.dll');
NET.addAssembly('C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.TCube.DCServoCLI.dll');

%Initialize Device List
import Thorlabs.MotionControl.DeviceManagerCLI.*
import Thorlabs.MotionControl.GenericMotorCLI.*
import Thorlabs.MotionControl.TCube.DCServoCLI.*

%Initialize Device List
DeviceManagerCLI.BuildDeviceList();
DeviceManagerCLI.GetDeviceListSize();

%Set up device and configuration
device = Thorlabs.MotionControl.TCube.DCServoCLI.TCubeDCServo.CreateTCubeDCServo(serial_num);
% device = TCubeDCServo.CreateTCubeDCServo(serial_num);
device.Connect(serial_num);
device.WaitForSettingsInitialized(5000);

% configure the stage
motorSettings = device.LoadMotorConfiguration(serial_num);
motorSettings.DeviceSettingsName = 'MTS25-Z8';
% update the RealToDeviceUnit converter
% motorSettings.UpdateCurrentConfiguration();

 % Set Velocity and Acceleration Parameters
velParams = device.GetVelocityParams();
velParams.MaxVelocity = 2.0;  % Replace with desired max velocity
velParams.Acceleration = 4.0; % Replace with desired acceleration
device.SetVelocityParams(velParams);

    % Set Limit Parameters (Max Velocity, Min Velocity, and Max Acceleration)
% motorDeviceSettings = device.MotorDeviceSettings;
% 
% % Get all properties of motorDeviceSettings
% props = properties(motorDeviceSettings);
% 
% % Loop through each property and display its name and value
% for i = 1:length(props)
%     propName = props{i};
%     try
%         propValue = motorDeviceSettings.(propName); % Access the property directly
%         fprintf('%s: ', propName);
%         disp(propValue); % Display property value, regardless of type
%     catch
%         fprintf('%s: Could not retrieve value\n', propName); % If inaccessible, print message
%     end
% end
% 

% Assuming motorDeviceSettings is already defined as:
motorDeviceSettings = device.MotorDeviceSettings;

%%Controls
motorDeviceSettings.Control.DefMaxVel=2.4;
motorDeviceSettings.Control.DefMinVel=1.0;
motorDeviceSettings.Control.DefAccn=2.0;

% Set Jogs - Velocity Profile
motorDeviceSettings.Jog.JogMinVel = 1.0; 
motorDeviceSettings.Jog.JogMaxVel = 2.4;   % Set Max Velocity for Jog
motorDeviceSettings.Jog.JogAccn = 2.0;  % Set Acceleration/Deceleration for Jog
motorDeviceSettings.Jog.JogStepSize = 1.0;             % Set Step Distance for Jogging


% Set Motor Physical Parameters
motorDeviceSettings.ThorlabsMotorPhysical.StepsPerRev = 512;  % Set Steps per Revolution
motorDeviceSettings.ThorlabsMotorPhysical.GearboxRatio = 67;  % Set Gearbox Ratio
motorDeviceSettings.ThorlabsMotorPhysical.Pitch = 1.0;
motorDeviceSettings.ThorlabsMotorPhysical.MinPosUnit = 0.0;
motorDeviceSettings.ThorlabsMotorPhysical.MaxPosUnit = 25.0;
motorDeviceSettings.ThorlabsMotorPhysical.RealUnits = 'mm';


% Update velocities in DriveArraySettings
motorDeviceSettings.MotorDriveSettingsArray.Velocity1 = System.Decimal(0.5);   % Set Velocity 1
motorDeviceSettings.MotorDriveSettingsArray.Velocity2 = System.Decimal(1.0);   % Set Velocity 2
motorDeviceSettings.MotorDriveSettingsArray.Velocity3 = System.Decimal(1.5);   % Set Velocity 3
motorDeviceSettings.MotorDriveSettingsArray.Velocity4 = System.Decimal(2.0);   % Set Velocity 4

% If there's an array of velocities, update it as well
%motorDriveSettingsArray.Velocities = System.Decimal([0.5, 1.0, 1.5, 2.0]);

% Set Backlash Correction
motorDeviceSettings.Misc.BacklashDistUnit = 0.00499942;      % Set Backlash Correction

% push the settings down to the device
%MotorDeviceSettings = device.MotorDeviceSettings;
device.SetSettings(motorDeviceSettings, false, true);
device.StartPolling(150);

pause(1); %wait to make sure device is enabled

device.Home(timeout_val);
fprintf('Motor homed in Y-Direction.\n');

yout = device;   % return motor object
end

