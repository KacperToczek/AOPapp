# import sys
# sys.path.insert(1, 'C:/Users/tocze/OneDrive/Dokumenty/studia/magisterka/semestr_4/IF2/Projekt 2/American_Options_Library/american_options')
# from underlying import Underlying
# from AMoption import Option
# import payoffs as am
import american_options.payoffs
import pandas as pd
import numpy as np
import dill
import chaospy
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from tabulate import tabulate
from django.contrib import messages
from django.shortcuts import redirect
from american_options import Underlying, Option
from american_options.payoffs import *
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

underlying_dictionary_path = os.path.join(current_dir, 'underlying_dictionary.pkl')
option_dictionary_path = os.path.join(current_dir, 'option_dictionary.pkl')
price_dictionary_path = os.path.join(current_dir, 'price_dictionary.pkl')


def home(request):
    with open(option_dictionary_path, 'rb') as fp:
        option_dictionary = dill.load(fp)

    option_choices = [(key, value) for key, value in option_dictionary.items()]

    with open(price_dictionary_path, 'rb') as fpp:
        price_dictionary = dill.load(fpp)

    data = []
    for k, v in price_dictionary.items():
        data.append([k, v])

    return render(request, 'home/home.html', {'title': 'Pricing', 'option_choices': option_choices, 'data': data})


def underlying(request):
    with open(underlying_dictionary_path, 'rb') as fp:
        underlying_dictionary = dill.load(fp)

    data = []
    for k, v in underlying_dictionary.items():
        data.append([k, vars(v)])

    with open(underlying_dictionary_path, 'wb') as fp:
        dill.dump(underlying_dictionary, fp)

    return render(request, 'home/underlying.html', {'title': 'Underlying', 'data': data})


def option(request):
    with open(underlying_dictionary_path, 'rb') as fp:
        underlying_dictionary = dill.load(fp)

    asset_choices = [(key, value) for key, value in underlying_dictionary.items()]

    with open(option_dictionary_path, 'rb') as fp:
        option_dictionary = dill.load(fp)

    data = []
    for k, v in option_dictionary.items():
        data.append([k, vars(v)])

    with open(option_dictionary_path, 'wb') as fp:
        dill.dump(option_dictionary, fp)

    return render(request, 'home/option.html', {'title': 'Option', 'asset_choices': asset_choices, 'data': data})


def clear_underlying_dictionary(request):
    if 'clear_underlying_dictionary' in request.POST:
        with open(underlying_dictionary_path, 'rb') as fp:
            underlying_dictionary = dill.load(fp)

        underlying_dictionary.clear()
        data = []
        for k, v in underlying_dictionary.items():
            data.append([k, vars(v)])

        with open(underlying_dictionary_path, 'wb') as fp:
            dill.dump(underlying_dictionary, fp)

        return render(request, 'home/underlying.html', {'data': data})
    else:
        return render(request, 'home/underlying.html')


def clear_option_dictionary(request):
    if 'clear_option_dictionary' in request.POST:
        with open(option_dictionary_path, 'rb') as fp:
            option_dictionary = dill.load(fp)

        option_dictionary.clear()
        data = []
        for k, v in option_dictionary.items():
            data.append([k, vars(v)])

        with open(option_dictionary_path, 'wb') as fp:
            dill.dump(option_dictionary, fp)

        return render(request, 'home/option.html', {'data': data})
    else:
        return render(request, 'home/option.html')


def clear_price_dictionary(request):
    if 'clear_price_dictionary' in request.POST:
        with open(price_dictionary_path, 'rb') as fp:
            price_dictionary = dill.load(fp)

        price_dictionary.clear()
        data = []

        with open(price_dictionary_path, 'wb') as fp:
            dill.dump(price_dictionary, fp)

        return render(request, 'home/home.html', {'data': data})
    else:
        return render(request, 'home/home.html')


def make_underlying(request):
    if request.method == 'POST':

        with open(underlying_dictionary_path, 'rb') as fp:
            underlying_dictionary = dill.load(fp)

        if not request.POST.get('asset_name'):
            messages.error(request, "Enter the asset name!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            asset_name = request.POST.get('asset_name')

        if not request.POST.get('spot_price'):
            messages.error(request, "Enter the spot price!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            spot_price = float(request.POST.get('spot_price'))

        if not request.POST.get('risk_free_rate'):
            messages.error(request, "Enter the risk-free rate!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            risk_free_rate = float(request.POST.get('risk_free_rate'))

        if not request.POST.get('volatility'):
            messages.error(request, "Enter the volatility!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            volatility = float(request.POST.get('volatility'))

        if not request.POST.get('vpy'):
            messages.error(request, "Enter the vpy!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            vpy = int(request.POST.get('vpy'))

        if not request.POST.get('time_steps'):
            messages.error(request, "Enter the time steps!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            time_steps = int(request.POST.get('time_steps'))

        if not request.POST.get('successors'):
            messages.error(request, "Enter the successors!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            successors = int(request.POST.get('successors'))

        if not request.POST.get('jump_intensity'):
            messages.error(request, "Enter the jump intensity!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            jump_intensity = float(request.POST.get('jump_intensity'))

        if not request.POST.get('param_a'):
            messages.error(request, "Enter the parameter a!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            param_a = float(request.POST.get('param_a'))

        if not request.POST.get('param_b'):
            messages.error(request, "Enter the parameter b!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            param_b = float(request.POST.get('param_b'))

        if not request.POST.get('mode_select'):
            messages.error(request, "Select the mode!")
            return render(request, 'home/underlying.html', {'messages': messages.get_messages(request)})
        else:
            mode_select = request.POST.get('mode_select')


        # define underlying
        asset = Underlying(spot_price=spot_price, r=risk_free_rate)

        # calibrate underlying
        if mode_select == "GBM":
            asset.calibrate_GBM(sigma=volatility, values_per_year_GBM=vpy)
        elif mode_select == "RT_GBM":
            asset.calibrate_RT_GBM(sigma=volatility, time_steps=time_steps, successors=successors)
        elif mode_select == "JD":
            asset.calibrate_JD(sigma=volatility, jump_intensity=jump_intensity, values_per_year_JD=vpy, a=param_a,
                               b=param_b)

        # save underlying
        underlying_dictionary[asset_name] = asset

        data = []
        for k, v in underlying_dictionary.items():
            data.append([k, vars(v)])

        with open(underlying_dictionary_path, 'wb') as fp:
            dill.dump(underlying_dictionary, fp)

        return render(request, 'home/underlying.html', {'data': data})
    else:
        return render(request, 'home/underlying.html')


def make_option(request):
    if request.method == 'POST':

        with open(underlying_dictionary_path, 'rb') as fp:
            underlying_dictionary = dill.load(fp)

        with open(option_dictionary_path, 'rb') as fp:
            option_dictionary = dill.load(fp)

        if not request.POST.get('option_name'):
            messages.error(request, "Enter the option name!")
            return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
        else:
            option_name = request.POST.get('option_name')

        if not request.POST.getlist('selected_keys'):
            messages.error(request, "Choose the asset(s)!")
            return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
        else:
            selected_keys = tuple(request.POST.getlist('selected_keys'))

        if not request.POST.get('maturity'):
            messages.error(request, "Enter the maturity!")
            return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
        else:
            maturity = float(request.POST.get('maturity'))

        assets_number = int(request.POST.get('assets_number'))

        if assets_number == 1:
            if not request.POST.get('payoff_select1d'):
                messages.error(request, "Choose the payoff!")
                return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
            else:
                payoff_select = request.POST.get('payoff_select1d')

            if request.POST.get('pd_select') == "True":
                pd_select = True
                if not request.POST.get('pd_type_select'):
                    messages.error(request, "Choose the path dependent type!")
                    return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
                else:
                    pd_type_select = request.POST.get('pd_type_select')
            else:
                pd_select = False
                pd_type_select = 'asian'

            if request.POST.get('barrier_select') == "True":
                barrier_select = True
                if not request.POST.get('barrier_type_select'):
                    messages.error(request, "Choose the barrier type!")
                    return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
                else:
                    barrier_type_select = request.POST.get('barrier_type_select')

                if not request.POST.get('barrier_level'):
                    messages.error(request, "Enter the barrier level!")
                    return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
                else:
                    barrier_level = float(request.POST.get('barrier_level'))
            else:
                barrier_select = False
                barrier_type_select = 'up-and-out'
                barrier_level = 0

            if payoff_select in ["bull_call", "bear_put"]:
                if not request.POST.get('strike_long'):
                    messages.error(request, "Enter the strike long!")
                    return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
                else:
                    strike_long = float(request.POST.get('strike_long'))
                if not request.POST.get('strike_short'):
                    messages.error(request, "Enter the strike short!")
                    return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
                else:
                    strike_short = float(request.POST.get('strike_short'))
            else:
                if not request.POST.get('strike1d'):
                    messages.error(request, "Enter the strike!")
                    return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
                else:
                    strike1d = float(request.POST.get('strike1d'))

            asset = underlying_dictionary[selected_keys[0]]

            def payoff_func(traj):
                if payoff_select == "call":
                    return payoff_creator_1d(traj, Call_Payoff, K=strike1d, barrier=barrier_select,
                                             barrier_level=barrier_level, barrier_type=barrier_type_select,
                                             path_dependent=pd_select, pd_type=pd_type_select)
                elif payoff_select == "put":
                    return payoff_creator_1d(traj, Put_Payoff, K=strike1d, barrier=barrier_select,
                                             barrier_level=barrier_level, barrier_type=barrier_type_select,
                                             path_dependent=pd_select, pd_type=pd_type_select)
                elif payoff_select == "square_call":
                    return payoff_creator_1d(traj, square_call, K=strike1d, barrier=barrier_select,
                                             barrier_level=barrier_level, barrier_type=barrier_type_select,
                                             path_dependent=pd_select, pd_type=pd_type_select)
                elif payoff_select == "straddle":
                    return payoff_creator_1d(traj, straddle_payoff, strike=strike1d, barrier=barrier_select,
                                             barrier_level=barrier_level, barrier_type=barrier_type_select,
                                             path_dependent=pd_select, pd_type=pd_type_select)
                elif payoff_select == "bear_put":
                    return payoff_creator_1d(traj, bear_put_payoff, barrier=barrier_select, barrier_level=barrier_level,
                                             barrier_type=barrier_type_select, path_dependent=pd_select,
                                             pd_type=pd_type_select, strike_long=strike_long, strike_short=strike_short)
                elif payoff_select == "bull_call":
                    return payoff_creator_1d(traj, bull_call_payoff, barrier=barrier_select, barrier_level=barrier_level,
                                             barrier_type=barrier_type_select, path_dependent=pd_select,
                                             pd_type=pd_type_select, strike_long=strike_long, strike_short=strike_short)

            new_option = Option(underlyings=asset, payoff_func=payoff_func, T=maturity)

        elif assets_number == 2:
            if not request.POST.get('payoff_select2d'):
                messages.error(request, "Choose the payoff!")
                return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
            else:
                payoff_select = request.POST.get('payoff_select2d')

            assets = tuple(underlying_dictionary[key] for key in selected_keys)

            if payoff_select == "ratio_spread":
                if not request.POST.get('asset1_weight'):
                    messages.error(request, "Enter the first asset weight!")
                    return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
                else:
                    asset1_weight = float(request.POST.get('asset1_weight'))
                if not request.POST.get('asset2_weight'):
                    messages.error(request, "Enter the second asset weight!")
                    return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
                else:
                    asset2_weight = float(request.POST.get('asset2_weight'))

                new_option = Option(underlyings=assets,
                                    payoff_func=lambda traj_list: ratio_spread_payoff(traj_list=traj_list,
                                                                                 asset1_weight=asset1_weight,
                                                                                 asset2_weight=asset2_weight),
                                    T=maturity)
            elif payoff_select == "spread":
                new_option = Option(underlyings=assets,
                                    payoff_func=lambda traj_list: spread_payoff(traj_list=traj_list), T=maturity)
            elif payoff_select == "double_mixed":
                if not request.POST.get('which'):
                    messages.error(request, "Choose the min/max!")
                    return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
                else:
                    which = request.POST.get('which')

                assets = tuple(underlying_dictionary[key] for key in selected_keys)

                assets_number = int(request.POST.get('assets_number', 0))
                strikes = []
                selections = []
                for i in range(1, assets_number + 1):
                    strike = float(request.POST.get(f'strike{i}', 0))
                    selection = request.POST.get(f'select{i}', 'call')
                    strikes.append(strike)
                    selections.append(selection)

                new_option = Option(underlyings=assets,
                                    payoff_func=lambda traj_list: multiple_mixed_payoff(traj_list=traj_list, K=strikes,
                                                                                        payoff_type=selections,
                                                                                        which=which), T=maturity)

        elif assets_number > 2:
            payoff_select = request.POST.get('payoff_select3d')

            if not request.POST.get('which'):
                messages.error(request, "Choose the min/max!")
                return render(request, 'home/option.html', {'messages': messages.get_messages(request)})
            else:
                which = request.POST.get('which')

            assets = tuple(underlying_dictionary[key] for key in selected_keys)

            assets_number = int(request.POST.get('assets_number', 0))
            strikes = []
            selections = []
            for i in range(1, assets_number + 1):
                strike = float(request.POST.get(f'strike{i}', 0))
                selection = request.POST.get(f'select{i}', 'call')
                strikes.append(strike)
                selections.append(selection)

            new_option = Option(underlyings=assets,
                                payoff_func=lambda traj_list: multiple_mixed_payoff(traj_list=traj_list, K=strikes,
                                                                                    payoff_type=selections,
                                                                                    which=which), T=maturity)

        # save option
        option_dictionary[option_name] = new_option

        data = []
        for k, v in option_dictionary.items():
            data.append([k, vars(v)])

        with open(option_dictionary_path, 'wb') as fp:
            dill.dump(option_dictionary, fp)

        with open(underlying_dictionary_path, 'rb') as fp:
            underlying_dictionary = dill.load(fp)

        asset_choices = [(key, value) for key, value in underlying_dictionary.items()]

        return render(request, 'home/option.html', {'data': data, 'asset_choices': asset_choices})
    else:
        return render(request, 'home/option.html')


def make_price(request):
    if request.method == 'POST':
        with open(option_dictionary_path, 'rb') as fp:
            option_dictionary = dill.load(fp)

        with open(price_dictionary_path, 'rb') as fpp:
            price_dictionary = dill.load(fpp)

        if not request.POST.get('selected_option'):
            messages.error(request, "Choose the option!")
            return render(request, 'home/home.html', {'messages': messages.get_messages(request)})

        if not request.POST.get('number_sim'):
            messages.error(request, "Enter the number of simulations!")
            return render(request, 'home/home.html', {'messages': messages.get_messages(request)})

        option_name = request.POST.get('selected_option')
        selected_option = option_dictionary[request.POST.get('selected_option')]
        number_sim = int(request.POST.get('number_sim'))
        method_select = request.POST.get('method_select')
        option_price = 0

        gbm_calibrated = [asset.GBM_calibrated for asset in selected_option.underlyings]
        jd_calibrated = [asset.JD_calibrated for asset in selected_option.underlyings]

        if method_select == "LS":
            if all(element == True for element in gbm_calibrated):
                option_price = selected_option.LS(mode="GBM", n_sims=number_sim)
            elif all(element == True for element in jd_calibrated):
                option_price = selected_option.LS(mode="JD", n_sims=number_sim)
            else:
                messages.error(request, "If you want to use the LS method, you should"
                                        " first calibrate the underlying asset(s) using the GBM or JD")
                return render(request, 'home/home.html', {'messages': messages.get_messages(request)})
        elif method_select == "RTM":
            if len(selected_option.underlyings) == 1:
                if selected_option.underlyings[0].RT_GBM_calibrated:
                    option_price = selected_option.RTM(mode="RT_GBM", n_sims=number_sim)
                else:
                    messages.error(request, "If you want to use the RTM method, you should"
                                            " first calibrate the underlying asset using the RT_GBM")
                    return render(request, 'home/home.html', {'messages': messages.get_messages(request)})
            else:
                messages.error(request, "If you want to use the RTM method, you should"
                                        " first create option with only one underlying!")
                return render(request, 'home/home.html', {'messages': messages.get_messages(request)})
        elif method_select == "ssp":
            if all(element == True for element in gbm_calibrated):
                option_price = selected_option.ssp(mode="GBM", n_sims=number_sim)
            elif all(element == True for element in jd_calibrated):
                option_price = selected_option.ssp(mode="JD", n_sims=number_sim)
            else:
                messages.error(request, "If you want to use the SSP method, you should"
                                        " first calibrate the underlying asset(s) using the GBM or JD")
                return render(request, 'home/home.html', {'messages': messages.get_messages(request)})

        #data = [[option_name, underlying_name, option_price]]

        if method_select == "RTM" and len(selected_option.underlyings)==1:
            str1 = option_price['left low'].to_string(index=False)
            str2 = option_price['righ high'].to_string(index=False)
            #str2 = option_price['right high'].to_string(index=False)
            interval = str1 + ' - ' + str2
            price_dictionary[option_name] = interval
        else:
            price_dictionary[option_name] = option_price

        data = []
        for k, v in price_dictionary.items():
            data.append([k, v])

        with open(price_dictionary_path, 'wb') as fpp:
            dill.dump(price_dictionary, fpp)

        return render(request, 'home/home.html', {'data': data})
    else:
        return render(request, 'home/home.html')





# def make_underlying(request):
#     if request.method == 'POST':
#
#         # we get the data from the form
#         spot_price = float(request.POST.get('spot_price'))
#         risk_free_rate = float(request.POST.get('risk_free_rate'))
#         mode_select = request.POST.get('mode_select')
#         volatility = float(request.POST.get('volatility'))
#         vpy = int(request.POST.get('vpy'))
#         time_steps = int(request.POST.get('time_steps'))
#         successors = int(request.POST.get('successors'))
#         data_hist = request.POST.get('data_hist')
#
#         strike = float(request.POST.get('strike'))
#         maturity = float(request.POST.get('maturity'))
#         payoff = request.POST.get('payoff')
#         pd_select = request.POST.get('pd_select')
#         pd_type_select = request.POST.get('pd_type_select')
#         barrier_select = request.POST.get('barrier_select')
#         barrier_level = float(request.POST.get('barrier_level'))
#         barrier_type_select = request.POST.get('barrier_type_select')
#
#         number_sim = int(request.POST.get('number_sim'))
#         method_select = request.POST.get('method_select')
#         n_bins = int(request.POST.get('n_bins'))
#
#         # we process data here
#
#         aktywo = Underlying(spot_price=spot_price, r=risk_free_rate)
#
#         if mode_select == "GBM":
#             aktywo.calibrate_GBM(sigma=volatility, values_per_year_GBM=vpy)
#         elif mode_select == "Binomial":
#             aktywo.calibrate_Binomial(sigma=volatility, time_steps=time_steps, successors=successors)
#         elif mode_select == "Bootstrap":
#             return HttpResponse("To pojawi się niedługo :)")
#
#         opcja = Option(underlyings=aktywo, strike=strike, payoff_func=lambda traj, strike: np.maximum(traj - strike, 0),
#                        T=maturity, barrier=barrier_select, barrier_level=barrier_level, barrier_type=barrier_type_select,
#                        path_dependent=pd_select, pd_type=pd_type_select)
#
#         # opcja = Option(underlyings=aktywo, strike=strike, payoff_func=lambda traj, strike: np.maximum(traj - strike, 0), T=maturity)
#
#         if method_select == "LS":
#             if mode_select == "GBM":
#                 option_price = opcja.LS(mode=mode_select, n_sims=number_sim)
#             else:
#                 return HttpResponse("Do LS musisz skalibrować za pomocą GBM")
#         elif method_select == "RTM":
#             if mode_select == "Binomial":
#                 option_price = opcja.RTM(mode=mode_select, n_sims=number_sim)[['left low', 'right high']]
#             else:
#                 return HttpResponse("Do RTM musisz skalibrować za pomocą Binomial")
#         elif method_select == "ssp":
#             if mode_select == "GBM":
#                 option_price = opcja.ssp(n=number_sim, n_bins=n_bins)
#             else:
#                 return HttpResponse("Do ssp musisz skalibrować za pomocą GBM")
#
#         data = []
#         # output
#         # data = [
#         #     ["Option Price", option_price],
#         #     ["", ""],
#         #     ["Spot Price", spot_price],
#         #     ["Risk-Free Rate", risk_free_rate],
#         #     ["Mode Select", mode_select],
#         #     ["Volatility", volatility],
#         #     ["VPY", vpy],
#         #     ["Time Steps", time_steps],
#         #     ["Successors", successors],
#         #     ["Data Hist", data_hist],
#         #     ["Strike", strike],
#         #     ["Maturity", maturity],
#         #     ["Payoff", payoff],
#         #     ["PD Select", pd_select],
#         #     ["PD Type Select", pd_type_select],
#         #     ["Barrier Select", barrier_select],
#         #     ["Barrier Level", barrier_level],
#         #     ["Barrier Type Select", barrier_type_select],
#         #     ["Number Sim", number_sim],
#         #     ["Method Select", method_select],
#         #     ["N Bins Input", n_bins]
#         # ]
#         L.append(aktywo)
#         for akt in L:
#             data.append(["Spot price", akt.spot_price])
#
#
#         return render(request, 'home/underlying.html', {'data': data})
#     else:
#         return render(request, 'home/underlying.html')
