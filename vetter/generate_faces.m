% Ilker Yildirim ilkery@mit.edu
baselpath = './PublicMM1';
baselmatlabpath = './PublicMM1/matlab';

addpath(baselpath);
addpath(baselmatlabpath);

[model, msz] = load_model();
counter = 1;

% generate a head and render it
dim = 50;
[shape, tex, tl, alpha, beta, model] = generate_head(dim);
global texMU
texMU = model.texMU;
global texPC
texPC = model.texPC;
global texEV
texEV = model.texEV;
rp     = defrp;
rp.phi = 0; %frontal
rp.elevation = pi/6; % pitch is zero (this is up-down angles)
rp.mode_az = 0; % azimuth of the light
rp.mode_el = 0; % elevation of the light
size(shape)
handle = display_face(shape, tex, model.tl, rp, rp.mode_az, rp.mode_el, []);
% plywrite('/Users/Janner/Desktop/coefTest.ply', shape, tex, tl)
% The code below generates faces in systematic variation of viewing
% conditions
% for i = 1:25
%     disp(i);
%     [shape, tex, tl] = generate_head();
%     % Render it
%     for phi = [0.0, 0.75, 1.25, -0.75, -1.25, 2, 3] % yaw
%         for elevation = [0.0]%[-0.25, 0.0, 0.25] % pitch
%             for mode_az = [0]%[-80, -50, 0, 50, 80] % light's azimuth
%                 for mode_el = [0]%[-80, -50, 0, 50, 80] % light's elevation
%                     rp     = defrp;
%                     if phi == 2 || phi == 3
%                         rp.phi = 0;
%                     else
%                         rp.phi = phi;
%                     end
%                     rp.dir_light.dir = [0;1;1];
%                     rp.dir_light.intens = 0.6*ones(3,1);
%                     if phi == 2
%                         rp.elevation = -0.25;
%                     elseif phi == 3
%                         rp.elevation = 0.25;
%                     else
%                         rp.elevation = elevation;
%                     end
%                     rp.mode_az = mode_az;
%                     rp.mode_el = mode_el;
%                     handle = display_face(shape, tex, model.tl, rp, rp.mode_az, rp.mode_el, []);
%                     print(handle, '-dpng','-r0', strcat('./images/', int2str(counter), '.png'));
%                     fprintf(fileID, '%d, %d, %d, %d, %d, %d\n', counter, i, phi, elevation, mode_az, mode_el);
%                     counter = counter + 1;
%                 end
%             end
%         end
%     end
% end


