%%%%%%%%%%%%%%%%%%初始化%%%%%%%%%%%%%%%%%
function ACO_ImageSegmentation
    filename = 'tigers';
    img = double(imread([filename '.bmp']))./255;

    % 如果图像是RGB图像，将其转换为灰度图像
    if size(img, 3) == 3
        img = rgb2gray(img);
    end

    [nrow, ncol] = size(img);
    v = zeros(size(img));
    v_norm = 0;

    for rr = 1:nrow
        for cc = 1:ncol
            temp1 = [rr-2 cc-1; rr-2 cc+1; rr-1 cc-2; rr-1 cc-1; rr-1 cc; rr-1 cc+1; rr-1 cc+2; rr cc-1];
            temp2 = [rr+2 cc+1; rr+2 cc-1; rr+1 cc+2; rr+1 cc+1; rr+1 cc; rr+1 cc-1; rr+1 cc-2; rr cc+1];
            temp0 = find(temp1(:, 1) >= 1 & temp1(:, 1) <= nrow & temp1(:,2) >= 1 & temp1(:,2) <= ncol & temp2(:, 1) >= 1 & temp2(:, 1) <= nrow & temp2(:,2) >= 1 & temp2(:,2) <= ncol);
            temp11 = temp1(temp0, :);
            temp22 = temp2(temp0, :);
            temp00 = zeros(size(temp11, 1));
            for kk = 1:size(temp11, 1)
                temp00(kk) = abs(img(temp11(kk, 1), temp11(kk, 2)) - img(temp22(kk, 1), temp22(kk, 2))); 
            end
            if isempty(temp11)
                v(rr, cc) = 0;
                v_norm = v_norm + v(rr, cc);
            else
                lambda = 100;
                temp00 = lambda .* temp00 .^ 4;
            end
            v(rr, cc) = sum(temp00); 
            v_norm = v_norm + v(rr, cc);
        end
    end

    v = v ./ v_norm;
    p = 0.0001 .* ones(size(img));
    alpha = 1;
    beta = 0.1;
    rho = 0.1;
    ant_total_num = round(sqrt(nrow * ncol));
    ant_pos_idx = zeros(ant_total_num, 2); 
    temp = rand(ant_total_num, 2);
    ant_pos_idx(:, 1) = round(1 + (nrow - 1) * temp(:, 1)); 
    ant_pos_idx(:, 2) = round(1 + (ncol - 1) * temp(:, 2)); 
    A = 40;
    memory_length = round(rand(1) * (0.3 * A) + 0.85 * A);
    ant_memory = zeros(ant_total_num, memory_length);
    total_step_num = 900;

    for step_idx = 1:total_step_num
        delta_p_current = zeros(nrow, ncol);
        for ant_idx = 1:ant_total_num
            ant_current_row_idx = ant_pos_idx(ant_idx, 1);
            ant_current_col_idx = ant_pos_idx(ant_idx, 2); 
            rr = ant_current_row_idx;
            cc = ant_current_col_idx;

            ant_search_range_temp = [rr-1 cc-1; rr-1 cc; rr-1 cc+1; rr cc-1; rr cc+1; rr+1 cc-1; rr+1 cc; rr+1 cc+1];
            temp = ant_search_range_temp(:, 1) >= 1 & ant_search_range_temp(:, 1) <= nrow & ant_search_range_temp(:, 2) >= 1 & ant_search_range_temp(:, 2) <= ncol;
            ant_search_range = ant_search_range_temp(temp, :); 
            ant_transit_prob_v = zeros(size(ant_search_range, 1), 1); 
            ant_transit_prob_p = zeros(size(ant_search_range, 1), 1); 
            for kk = 1:size(ant_search_range, 1)
                temp = (ant_search_range(kk, 1) - 1) * ncol + ant_search_range(kk, 2); 
                if isempty(find(ant_memory(ant_idx, :) == temp, 1))
                    ant_transit_prob_v(kk) = v(ant_search_range(kk, 1), ant_search_range(kk, 2));
                    ant_transit_prob_p(kk) = p(ant_search_range(kk, 1), ant_search_range(kk, 2)); 
                else
                    ant_transit_prob_v(kk) = 0; 
                    ant_transit_prob_p(kk) = 0;
                end
            end
            if (sum(ant_transit_prob_v) == 0) || (sum(ant_transit_prob_p) == 0)
                for kk = 1:size(ant_search_range, 1)
                    ant_transit_prob_v(kk) = v(ant_search_range(kk, 1), ant_search_range(kk, 2));
                    ant_transit_prob_p(kk) = p(ant_search_range(kk, 1), ant_search_range(kk, 2));
                end
            end
            ant_transit_prob = (ant_transit_prob_v .^ alpha) .* (ant_transit_prob_p .^ beta) ./ (sum((ant_transit_prob_v .^ alpha) .* (ant_transit_prob_p .^ beta)));

            temp = find(cumsum(ant_transit_prob) >= rand(1), 1);
            ant_next_row_idx = ant_search_range(temp, 1);
            ant_next_col_idx = ant_search_range(temp, 2);
            if isempty(ant_next_row_idx)
                ant_next_row_idx = ant_current_row_idx;
                ant_next_col_idx = ant_current_col_idx;
            end
            ant_pos_idx(ant_idx, 1) = ant_next_row_idx;
            ant_pos_idx(ant_idx, 2) = ant_next_col_idx;
            delta_p_current(ant_pos_idx(ant_idx, 1), ant_pos_idx(ant_idx, 2)) = 1; 
            if step_idx <= memory_length
                ant_memory(ant_idx, step_idx) = (ant_pos_idx(ant_idx, 1) - 1) * ncol + ant_pos_idx(ant_idx, 2);
            elseif step_idx > memory_length
                ant_memory(ant_idx, :) = circshift(ant_memory(ant_idx, :), [0 -1]); 
                ant_memory(ant_idx, end) = (ant_pos_idx(ant_idx, 1) - 1) * ncol + ant_pos_idx(ant_idx, 2);
            end

            p = ((1 - rho) .* p + rho .* delta_p_current .* v) .* delta_p_current + p .* (abs(1 - delta_p_current));
        end
    end

    T = judge(p);
    imwrite(uint8(abs((p >= 0.8 * T) * 255 - 255)), gray(256), [filename '_edge_aco_' '.bmp'], 'bmp');
end

function tt = judge(I) 
    I = I(:);
    [counts, N] = hist(I, 256); 
    i = 1;
    mu = cumsum(counts);
    T(i) = (sum(N .* counts)) / mu(end);
    mu2 = cumsum(counts(N <= T(i)));
    MBT = sum(N(N <= T(i)) .* counts(N <= T(i))) / mu2(end);
    mu3 = cumsum(counts(N > T(i)));
    MAT = sum(N(N > T(i)) .* counts(N > T(i))) / mu3(end);
    i = i + 1;
    T(i) = (MAT + MBT) / 2;
    Threshold = T(i);
    while abs(T(i) - T(i-1)) >= 1
        mu2 = cumsum(counts(N <= T(i)));
        MBT = sum(N(N <= T(i)) .* counts(N <= T(i))) / mu2.end;
        mu3 = cumsum(counts(N > T(i)));
        MAT = sum(N(N > T(i)) .* counts(N > T(i))) / mu3.end; 
        i = i + 1;
        T(i) = (MAT + MBT) / 2;
        Threshold = T(i);
    end
    tt = Threshold;
end



