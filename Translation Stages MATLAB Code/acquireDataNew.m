clear all;
close all;
clc;


% --------------------------------------------------
% This was done using the OWON Oscillscope
% --------------------------------------------------
timeout_val = 60000;
TDC_serial_num = '83816594'; % Serial number on the TDC controller
KDC_serial_num = '27269557'; % Serial number on the KDC controller

% Variables to track resources
motorX_connected = false;
motorY_connected = false;
oscilloscope_connected = false;

try
    % Create motor object
    motorX = KDC101(KDC_serial_num, timeout_val);
    motorX_connected = true;

    motorY = TDC001(TDC_serial_num, timeout_val);
    motorY_connected = true;

    % Connect to the oscilloscope
    address = 'USB0::0x5345::0x1235::2318021::0::INSTR';
    resource = visa('NI', address);
    resource.Timeout = 60;
    resource.InputBufferSize = 1000000;
    fopen(resource);
    oscilloscope_connected = true;

    % Query and print oscilloscope ID
    fprintf(resource, '*IDN?');
    idn_response = fscanf(resource);
    fprintf("Connected to oscilloscope: %s\n", strtrim(idn_response));

    % Set up the oscilloscope
    fprintf(resource, ':CH1:SCALE 500mV');
    fprintf(resource, ':CH1:OFFSET 0V');
    fprintf(resource, ':CH1:COUPLING DC');
    fprintf(resource, ':CH1:DISP ON');

    fprintf(resource, ':CH4:SCALE 500mV');
    fprintf(resource, ':CH4:OFFSET 0V');
    fprintf(resource, ':CH4:COUPLING DC');
    fprintf(resource, ':CH4:DISP ON');

    fprintf(resource, ':HORIZONTAL:SCALE 500uS');
    fprintf(resource, ':HORIZONTAL:OFFSET 0');

    fprintf(resource, ':TRIGGER:SINGLE:EDGE:SOURCE CH4');
    fprintf(resource, ':TRIG:SING:MODE EDGE');
    fprintf(resource, ':TRIGger:SINGle:EDGE:COUPling DC');
    fprintf(resource, ':TRIGger:SINGle:EDGE:SLOPe RISE');
    fprintf(resource, ':TRIGGER:SINGLE:EDGE:LEVEL 0.2');
    fprintf(resource, ':TRIGger:SINGle:SWEep AUTO');

    % Fetch and validate configuration
    fprintf(resource, ':WAVeform:PREamble?');
    preamble = fscanf(resource);
    fprintf("Preamble Data: %s\n", preamble);

    % Voltage conversion parameters
    adc_resolution = 4096; % Assuming 12-bit ADC
    voltage_scale = 0.5; % 500mV/div from preamble
    vertical_offset = 0.0; % No offset
    sample_rate = 1E6; % 1 MS/s from preamble
    time_per_sample = 1 / sample_rate;
    range_points = 10000; % Ensure consistency with :WAVeform:RANGe

    % Define motor movement parameters
    step_size = 0.08; % Step size in mm
    delay_between_steps = 0.2; % Delay between steps in seconds
    count = 1;

    for stepY = 0.08:step_size:4
        for stepX = 0.08:step_size:4
            % Clear residual data
            fscanf(resource);

            % Fetch data for CH4 (Static Photodetector)
            fprintf(resource, ':WAVeform:BEGin CH4');
            fprintf(resource, ':WAVeform:RANGe 0,%d', range_points);
            fprintf(resource, ':WAVeform:FETCh? CH4');
            rawData_CH4 = binblockread(resource, 'int16');
            fprintf(resource, ':WAVeform:END');

            voltage_data_CH4 = (double(rawData_CH4) / adc_resolution) * voltage_scale + vertical_offset;

            % Fetch data for CH1 (Moving Photodetector)
            fprintf(resource, ':WAVeform:BEGin CH1');
            fprintf(resource, ':WAVeform:RANGe 0,%d', range_points);
            fprintf(resource, ':WAVeform:FETCh? CH1');
            rawData_CH1 = binblockread(resource, 'int16');
            fprintf(resource, ':WAVeform:END');

            voltage_data_CH1 = (double(rawData_CH1) / adc_resolution) * voltage_scale + vertical_offset;

            % Create time vector for both channels
            reference_time = (0:length(voltage_data_CH4) - 1) * time_per_sample;

            % Save data for CH4
            csv_file_CH4 = sprintf('1K_reference_%d.csv', count);
            fileID = fopen(csv_file_CH4, 'w');
            fprintf(fileID, 'Time (s),Voltage (V)\n');
            for i = 1:length(voltage_data_CH4)
                fprintf(fileID, '%.6f, %.6f\n', reference_time(i), voltage_data_CH4(i));
            end
            fclose(fileID);

            % Save data for CH1
            csv_file_CH1 = sprintf('1K_oscilloscope_waveform_%d.csv', count);
            fileID = fopen(csv_file_CH1, 'w');
            fprintf(fileID, 'Time (s),Voltage (V)\n');
            for i = 1:length(voltage_data_CH1)
                fprintf(fileID, '%.6f, %.6f\n', reference_time(i), voltage_data_CH1(i));
            end
            fclose(fileID);

            % Move the motors
            pause(delay_between_steps);
            motorX.MoveTo(stepX, timeout_val);
            posX = System.Decimal.ToDouble(motorX.Position);
            fprintf('The stage position in X is %.2f mm.\n', posX);
            fprintf('The counter value is %d.\n', count);

            count = count + 1;
        end
        motorX.Home(timeout_val);
        motorY.MoveTo(stepY, timeout_val);
        posY = System.Decimal.ToDouble(motorY.Position);
        fprintf('The stage position in Y is %.2f mm.\n', posY);
    end
catch ME
    fprintf('An error occurred: %s\n', ME.message);
end

% Cleanup resources
if motorX_connected
    try
        motorX.StopPolling();
        motorX.Disconnect();
    catch motorError
        fprintf('Error disconnecting motor X: %s\n', motorError.message);
    end
end

if motorY_connected
    try
        motorY.StopPolling();
        motorY.Disconnect();
    catch motorError
        fprintf('Error disconnecting motor Y: %s\n', motorError.message);
    end
end

if oscilloscope_connected
    try
        fclose(resource);
        delete(resource);
    catch oscError
        fprintf('Error disconnecting oscilloscope: %s\n', oscError.message);
    end
end

clear resource;
