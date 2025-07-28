%% Header
% Title: KDC101.m
% Created Date: 2024-01-16
% Last modified date: 2024-07-02
% Matlab Version: R2023b
% Thorlabs DLL version: Kinesis 1.14.44
%% Notes:
%
% Example for the KDC101 using the PRM1/M-Z8 stage

%% Start of code
function yout = KDC101(serialNumber, timeout_val)

%% Add and Import Assemblies
devCLI = NET.addAssembly('C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.DeviceManagerCLI.dll');
genCLI = NET.addAssembly('C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.GenericMotorCLI.dll');
motCLI = NET.addAssembly('C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.KCube.DCServoCLI.dll');

import Thorlabs.MotionControl.DeviceManagerCLI.*
import Thorlabs.MotionControl.GenericMotorCLI.*
import Thorlabs.MotionControl.KCube.DCServoCLI.*

%% Connect
%Build Device List loads the connected devices to available memory
DeviceManagerCLI.BuildDeviceList();


% Connect to the controller
device = KCubeDCServo.CreateKCubeDCServo(serialNumber);
device.Connect(serialNumber);

try
    % Try/Catch statement used to disconnect correctly after an error

    device.WaitForSettingsInitialized(5000);
    device.StartPolling(250);
    
    %Pull the enumeration values from the DeviceManagerCLI
    optionTypeHandle = devCLI.AssemblyHandle.GetType('Thorlabs.MotionControl.DeviceManagerCLI.DeviceSettingsSectionBase+SettingsUseOptionType');
    optionTypeEnums = optionTypeHandle.GetEnumValues(); 
    
    %Load Settings to the controller
    motorConfiguration = device.LoadMotorConfiguration(serialNumber);
    motorConfiguration.LoadSettingsOption = optionTypeEnums.Get(1); % File Settings Option
    motorConfiguration.DeviceSettingsName = 'MTS25-Z8'; %The actuator type needs to be set here. This specifically loads an PRM1-Z8
    factory = KCubeMotor.KCubeDCMotorSettingsFactory();

    % update the RealToDeviceUnit converter
    %motorSettings.UpdateCurrentConfiguration();
    
     % Set Velocity and Acceleration Parameters
    velParams = device.GetVelocityParams();
    velParams.MaxVelocity = 2.0;  % Replace with desired max velocity
    velParams.Acceleration = 4.0; % Replace with desired acceleration
    device.SetVelocityParams(velParams);
    
    % Set Limit Parameters (Max Velocity, Min Velocity, and Max Acceleration)
    % motorDeviceSettings = device.MotorDeviceSettings;
    
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

    % Assuming motorDeviceSettings is already defined as:
    motorDeviceSettings = device.MotorDeviceSettings;
    
    %%Controls
    motorDeviceSettings.Control.DefMaxVel=2.4;
    motorDeviceSettings.Control.DefMinVel=1.0;
    motorDeviceSettings.Control.DefAccn=2.0;
    
    % Set Jogs - Velocity Profile
    motorDeviceSettings.Jog.JogMinVel = 1.0; 
    motorDeviceSettings.Jog.JogMaxVel = 2.4;   % Set Max Velocity for Jog
    motorDeviceSettings.Jog.JogAccn = 2.0;     % Set Acceleration/Deceleration for Jog
    motorDeviceSettings.Jog.JogStepSize = 1.0; % Set Step Distance for Jogging
    
    
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
    
    % Set Backlash Correction
    motorDeviceSettings.Misc.BacklashDistUnit = 0.00499942;      % Set Backlash Correction

    device.SetSettings(factory.GetSettings(motorConfiguration), false, true);
    
    % Enable the device and start sending commands
    device.EnableDevice();
    pause(1); %wait to make sure the cube is enabled
    
    % Home the stage
    fprintf("Homing stage in X-Direction...\n")
    device.Home(timeout_val);
    fprintf("Homed\n\n")
    
catch e
    fprintf("Error has caused the program to stop, disconnecting..\n")
    fprintf(e.identifier);
    fprintf("\n");
    fprintf(e.message);
end
yout = device;   % return motor object
end