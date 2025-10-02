import random
import re
def generate_labeled_hedge_paragraph(
    has_active_derivative,
    swap_type=None,
    year_range=(1999, 2025),
    max_past_years=random.randint(1, 3),
    max_len=random.randint(4, 7),
    include_policy=None,
    company_name=None,
):
    """
    Generate a synthetic hedge paragraph with known label.

    Args:
        has_active_derivative (bool or None):
            - True: firm has active derivative in reporting year (label=0)
            - False: firm does not have active derivative (label=1)
            - None: policy/disclosure only, no specific positions (label=2)
        year_range (tuple): (min_year, max_year) for the reporting year
        max_past_years (int): Max number of prior years to include
        max_len (int): Maximum number of sentences
        include_policy (bool): Whether to include policy sentences with labels 0/1
                              If None, randomly decides (70% chance)

    Returns:
        tuple: (paragraph_text, label) where label is 0, 1, 8, 9, 10, 11, 12, 13 or 2
    """

    # Decide whether to include policy statements for labels 0 and 1
    if include_policy is None:
        include_policy = random.random() < 0.7

    # If label 2 (policy only), override to ensure policy is included
    if has_active_derivative is None:
        include_policy = True

    if company_name is None:
        # ~ 75% chance of company name
        if random.random() < 0.75:
            company_name = random.choice(company_names)
        else:
            company_name = random.choice(["The Company", "We"])
    if swap_type is None:
        swap_types = all_derivatives
    else:
        swap_types = derivative_keywords[swap_type]
    money_units = random.choice(money_unit_list)
    currency_code = random.choice(currency_codes)
    major_currency = random.choice(all_currencies)
    # Set up years
    current_year = random.randint(year_range[0], year_range[1])
    reporting_year = current_year
    num_past_years = random.randint(1, max_past_years)
    past_years = sorted(
        random.sample(range(current_year - 5, current_year), num_past_years)
    )

    all_sentences = []

    # Label 2: Policy/disclosure only (no specific positions)
    if has_active_derivative is None:
        # Context (0-1)
        if random.random() < 0.6:
            template = random.choice(context_templates)
            all_sentences.append(
                template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                )
            )

        # Impact (0-1)
        if random.random() < 0.7:
            template = random.choice(impact_templates)
            verb = random.choice(impact_verbs)
            all_sentences.append(
                template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=random.choice(months),
                    verb=verb,
                )
            )

        # Mitigation (0-1)
        if random.random() < 0.8:
            template = random.choice(mitigation_templates)
            verb = random.choice(mitigation_verbs)
            all_sentences.append(
                template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=random.choice(months),
                    verb=verb,
                    swap_type=random.choice(swap_types),
                )
            )

        # Accounting policy (always)
        act_template = random.choice(accounting_policy_templates)
        all_sentences.append(
            act_template.format(
                company=company_name,
                currency_code=currency_code,
                major_currency=major_currency,
                money_unit=money_units,
                end_day=random.randint(28, 31),
                swap_type=random.choice(swap_types),
                hedge_type=random.choice(hedge_types),
            )
        )

        # Documentation (0-1)
        if random.random() < 0.6:
            template = random.choice(documentation_templates)
            all_sentences.append(
                template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    hedge_type=random.choice(hedge_types),
                )
            )

        # Effectiveness (0-1)
        if random.random() < 0.7:
            template = random.choice(effectiveness_templates)
            sentence = template.format(
                company=company_name,
                currency_code=currency_code,
                major_currency=major_currency,
                money_unit=money_units,
                end_day=random.randint(28, 31),
                month=random.choice(months),
                hedge_type=random.choice(hedge_types),
                swap_type=random.choice(swap_types),
                metric=random.choice(metrics),
                frequency=random.choice(frequencies),
                verb=random.choice(assessment_verbs),
                method=random.choice(methods),
                standard=random.choice(standards),
            )
            all_sentences.append(sentence)

        # Ineffectiveness (0-1)
        if random.random() < 0.5:
            template = random.choice(ineffectiveness_templates)
            all_sentences.append(
                template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=random.choice(months),
                    frequency=random.choice(frequencies),
                )
            )

        # Discontinuation (0-1)
        if random.random() < 0.5:
            template = random.choice(discontinuation_templates)
            all_sentences.append(
                template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                )
            )

        # Currency description (0-1)
        if random.random() < 0.6:
            selected_currencies = []
            selected_currencies.extend(
                random.sample(major_currencies, random.randint(2, 4))
            )
            if random.random() < 0.5:
                selected_currencies.extend(
                    random.sample(european_currencies, random.randint(1, 2))
                )
            if random.random() < 0.4:
                selected_currencies.extend(
                    random.sample(asian_currencies, random.randint(1, 2))
                )
            if random.random() < 0.3:
                selected_currencies.extend(
                    random.sample(americas_currencies, random.randint(1, 2))
                )

            selected_currencies = list(dict.fromkeys(selected_currencies))
            currency_list = (
                ", ".join(selected_currencies[:-1]) + " and " + selected_currencies[-1]
            )
            if random.random() < 0.3:
                currency_list += " and other European and Latin American currencies"
            template = random.choice(currency_templates)
            all_sentences.append(
                template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=random.choice(months),
                    currencies=currency_list,
                )
            )

        # Alternative management (0-1)
        if random.random() < 0.4:
            template = random.choice(alternative_management_templates)
            all_sentences.append(
                template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                )
            )

        # {hedge_type} hedge (0-1)
        if random.random() < 0.5:
            template = random.choice(net_investment_templates)
            verb = random.choice(net_investment_verbs)
            all_sentences.append(
                template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=random.choice(months),
                    verb=verb,
                    hedge_type=random.choice(hedge_types),
                    swap_type=random.choice(swap_types),
                )
            )

        # Counterparty risk (0-1)
        if random.random() < 0.6:
            template = random.choice(counterparty_templates)
            all_sentences.append(
                template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                )
            )

        # No trading policy (always)
        nt_template = random.choice(no_trading_templates)
        all_sentences.append(
            nt_template.format(
                company=company_name,
                currency_code=currency_code,
                major_currency=major_currency,
                money_unit=money_units,
                end_day=random.randint(28, 31),
                month=random.choice(months),
                swap_type=random.choice(swap_types),
            )
        )

        label = 2

    # Labels 0 and 1: Event-based with optional policy statements
    else:
        # Generate past year sentences
        past_sentences = []
        for y in past_years:
            template = random.choice(past_event_templates)
            loss_amt = round(random.uniform(20, 35), 1)
            swap_type = random.choice(swap_types)
            month = random.choice(months)
            sentence = template.format(
                company=company_name,
                currency_code=currency_code,
                major_currency=major_currency,
                money_unit=money_units,
                end_day=random.randint(28, 31),
                month=month,
                year=y,
                next_year=y + 1,
                hedge_type=random.choice(hedge_types),
                amount=loss_amt,
                swap_type=swap_type,
                quarter=random.choice(quarters),
            )
            past_sentences.append(sentence)

        # Sentences about entering swaps
        swap_entry_sentences = []

        if has_active_derivative:
            # Label 0: Active derivatives
            for _ in range(random.randint(1, 2)):
                template = random.choice(swap_entry_templates)
                notional = round(random.uniform(200, 550), 0)
                swap_type = random.choice(swap_types)
                month = random.choice(months)
                sentence = template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=month,
                    year=current_year,
                    swap_type=swap_type,
                    notional=notional,
                    quarter=random.choice(quarters),
                )
                swap_entry_sentences.append(sentence)

            # Add ongoing position indicators
            for _ in range(random.randint(1, 2)):
                template = random.choice(active_position_templates)
                notional = round(random.uniform(300, 800), 0)
                swap_type = random.choice(swap_types)
                sentence = template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=month,
                    year=current_year,
                    swap_type=swap_type,
                    notional=notional,
                )
                swap_entry_sentences.append(sentence)
        else:
            # Label 1: No active derivatives
            for y in past_years:
                if random.random() < 0.6:
                    template = random.choice(swap_entry_templates)
                    notional = round(random.uniform(200, 550), 0)
                    swap_type = random.choice(swap_types)
                    month = random.choice(months)
                    sentence = template.format(
                        company=company_name,
                        currency_code=currency_code,
                        major_currency=major_currency,
                        money_unit=money_units,
                        end_day=random.randint(28, 31),
                        month=month,
                        year=y,
                        quarter=random.choice(quarters),
                        swap_type=swap_type,
                        notional=notional,
                    )
                    swap_entry_sentences.append(sentence)

            # Add termination sentences
            if random.random() < 0.7:
                template = random.choice(termination_templates)
                q = random.choice(quarters)
                swap_type = random.choice(swap_types)
                sentence = template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    quarter=q,
                    month=random.choice(months),
                    year=current_year,
                    swap_type=swap_type,
                )
                swap_entry_sentences.append(sentence)

            if random.random() < 0.5:
                template = random.choice(expiration_templates)
                month = random.choice(months)
                swap_type = random.choice(swap_types)
                quarter = random.choice(quarters)
                sentence = template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=month,
                    year=current_year,
                    swap_type=swap_type,
                    quarter=quarter,
                )
                swap_entry_sentences.append(sentence)

        # Quarterly events
        quarter_sentences = []
        num_events = random.randint(0, 2)

        for _ in range(num_events):
            template = random.choice(quarterly_event_templates)
            q = random.choice(quarters)

            if has_active_derivative:
                year_event = random.choice(past_years + [current_year])
            else:
                year_event = random.choice(past_years)

            notional = round(random.uniform(200, 800), 0)
            settlement = round(random.uniform(50, 200), 0)
            swap_type = random.choice(swap_types)

            sentence = template.format(
                company=company_name,
                currency_code=currency_code,
                major_currency=major_currency,
                money_unit=money_units,
                end_day=random.randint(28, 31),
                quarter=q,
                year=year_event,
                notional=notional,
                settlement=settlement,
                swap_type=swap_type,
                month=random.choice(months),
            )
            quarter_sentences.append(sentence)

        # Add event-based sentences
        all_sentences.extend(past_sentences)
        all_sentences.extend(swap_entry_sentences)
        all_sentences.extend(quarter_sentences)

        # Option contract sentences (0-1)
        if random.random() < 0.3:
            template = random.choice(option_contract_templates)
            swap_type = random.choice(
                [
                    "foreign currency purchased put option contracts",
                    "purchased put option contracts",
                    "purchased call option contracts",
                ]
            )

            notional1 = round(random.uniform(0, 300), 0)  # Can be 0 for current year
            notional2 = round(random.uniform(100, 400), 0)
            sentence = template.format(
                company=company_name,
                currency_code=currency_code,
                major_currency=major_currency,
                money_unit=money_units,
                end_day=random.randint(28, 31),
                month=random.choice(months),
                swap_type=swap_type,
                notional1=notional1,
                notional2=notional2,
                year=current_year,
                prev_year=current_year - 1,
            )
            all_sentences.append(sentence)

        # Dedesignation sentences (0-1) - more common for Label 1
        dedesignation_chance = 0.2 if has_active_derivative else 0.5
        if random.random() < dedesignation_chance:
            template = random.choice(dedesignation_templates)
            swap_type = random.choice(swap_types)
            q = random.choice(quarters)
            sentence = template.format(
                company=company_name,
                currency_code=currency_code,
                major_currency=major_currency,
                money_unit=money_units,
                end_day=random.randint(28, 31),
                swap_type=swap_type,
                year=current_year,
                quarter=q,
                month=random.choice(months),
            )
            all_sentences.append(sentence)

        # Forward starting/treasury lock sentences (0-1)
        if random.random() < 0.3:
            template = random.choice(forward_starting_templates)
            swap_type = random.choice(
                [
                    "forward starting interest rate swaps",
                    "treasury rate lock agreements",
                    "forward starting swaps or treasury rate lock agreements",
                ]
            )
            sentence = template.format(
                company=company_name,
                currency_code=currency_code,
                major_currency=major_currency,
                money_unit=money_units,
                end_day=random.randint(28, 31),
                month=random.choice(months),
                swap_type=swap_type,
                hedge_type=random.choice(hedge_types),
            )
            all_sentences.append(sentence)

        # Collar strategy sentences (0-1)
        if random.random() < 0.2:
            template = random.choice(collar_strategy_templates)
            swap_type = random.choice(
                [
                    "purchased put and call options",
                    "foreign currency options",
                    "option contracts",
                ]
            )
            collar_year = random.choice(past_years)
            if has_active_derivative:
                collar_year = current_year
            sentence = template.format(
                company=company_name,
                currency_code=currency_code,
                major_currency=major_currency,
                money_unit=money_units,
                end_day=random.randint(28, 31),
                swap_type=swap_type,
                quarter=random.choice(quarters),
                month=random.choice(months),
                year=collar_year,
            )
            all_sentences.append(sentence)
        # Fair value position statements (0-1) - mainly for Label 0 (active derivatives)

        if has_active_derivative is True or has_active_derivative is None:
            if random.random() < 0.3:
                template = random.choice(fair_value_position_templates)
                swap_type = random.choice(swap_types)
                amount = round(random.uniform(2, 50), 1)
                oci_amount = round(
                    amount * random.uniform(0.05, 0.15), 1
                )  # OCI is typically smaller
                position_type = random.choice(position_types)
                oci_action = random.choice(oci_actions)

                sentence = template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=random.choice(months),
                    year=current_year,
                    swap_type=swap_type,
                    position_type=position_type,
                    amount=amount,
                    oci_amount=oci_amount,
                    oci_action=oci_action,
                )
                all_sentences.append(sentence)

        # Specific hedge designation with currency pairs (0-1) - mainly for Label 0

        if has_active_derivative is True:
            if random.random() < 0.25:
                template = random.choice(specific_hedge_templates)
                swap_type = random.choice(
                    [
                        "forward purchases",
                        "forward contracts",
                        "currency forwards",
                        "foreign exchange forwards",
                    ]
                )
                notional_currency = random.choice(currency_codes)
                notional_amount = random.randint(100, 500)
                expiry_year = current_year + 1
                currency_pair = random.choice(currency_pairs)
                hedged_item = random.choice(hedged_items)

                sentence = template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=random.choice(months),
                    swap_type=swap_type,
                    notional_currency=notional_currency,
                    notional_amount=notional_amount,
                    expiry_year=expiry_year,
                    currency_pair=currency_pair,
                    hedged_item=hedged_item,
                )
                all_sentences.append(sentence)
            # Cash pooling arrangements (0-1) - can appear in any label
            if random.random() < 0.15:
                template = random.choice(cash_pooling_templates)
                all_sentences.append(
                    template.format(
                        company=company_name,
                        currency_code=currency_code,
                        major_currency=major_currency,
                        money_unit=money_units,
                        end_day=random.randint(28, 31),
                    )
                )

            # Debt optimization strategies (0-1) - can appear in any label
            if random.random() < 0.2:
                template = random.choice(debt_optimization_templates)
                instrument_list = random.choice(instrument_lists)
                sentence = template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=random.choice(months),
                    instrument_list=instrument_list,
                )
                all_sentences.append(sentence)
        # Optionally add policy statements to prevent overfitting
        if include_policy:
            policy_sentences = []

            # Context (0-1)
            if random.random() < 0.3:
                template = random.choice(context_templates)
                policy_sentences.append(
                    template.format(
                        company=company_name,
                        currency_code=currency_code,
                        major_currency=major_currency,
                        money_unit=money_units,
                        end_day=random.randint(28, 31),
                    )
                )

            # Impact (0-1)
            if random.random() < 0.3:
                template = random.choice(impact_templates)
                verb = random.choice(impact_verbs)
                policy_sentences.append(
                    template.format(
                        company=company_name,
                        currency_code=currency_code,
                        major_currency=major_currency,
                        money_unit=money_units,
                        end_day=random.randint(28, 31),
                        month=random.choice(months),
                        verb=verb,
                    )
                )

            # Mitigation (0-1)
            if random.random() < 0.4:
                template = random.choice(mitigation_templates)
                verb = random.choice(mitigation_verbs)
                policy_sentences.append(
                    template.format(
                        company=company_name,
                        currency_code=currency_code,
                        major_currency=major_currency,
                        money_unit=money_units,
                        end_day=random.randint(28, 31),
                        month=random.choice(months),
                        verb=verb,
                        swap_type=random.choice(swap_types),
                    )
                )

            # Accounting policy (0-1)
            if random.random() < 0.5:
                template = random.choice(accounting_policy_templates)
                policy_sentences.append(
                    template.format(
                        company=company_name,
                        currency_code=currency_code,
                        major_currency=major_currency,
                        money_unit=money_units,
                        hedge_type=random.choice(hedge_types),
                        swap_type=random.choice(swap_types),
                    )
                )

            # Documentation (0-1)
            if random.random() < 0.3:
                template = random.choice(documentation_templates)
                policy_sentences.append(
                    template.format(
                        company=company_name,
                        currency_code=currency_code,
                        major_currency=major_currency,
                        money_unit=money_units,
                        hedge_type=random.choice(hedge_types),
                    )
                )

            # Effectiveness (0-1)
            if random.random() < 0.4:
                template = random.choice(effectiveness_templates)
                # Provide all possible placeholders
                sentence = template.format(
                    company=company_name,
                    currency_code=currency_code,
                    major_currency=major_currency,
                    money_unit=money_units,
                    end_day=random.randint(28, 31),
                    month=random.choice(months),
                    hedge_type=random.choice(hedge_types),
                    metric=random.choice(metrics),
                    frequency=random.choice(frequencies),
                    verb=random.choice(assessment_verbs),
                    method=random.choice(methods),
                    standard=random.choice(standards),
                    swap_type=random.choice(swap_types),
                )
                policy_sentences.append(sentence)

            # Currency description (0-1)
            if random.random() < 0.3:
                selected_currencies = []
                selected_currencies.extend(
                    random.sample(major_currencies, random.randint(2, 3))
                )
                if random.random() < 0.4:
                    selected_currencies.extend(
                        random.sample(european_currencies, random.randint(1, 2))
                    )

                selected_currencies = list(dict.fromkeys(selected_currencies))
                currency_list = (
                    ", ".join(selected_currencies[:-1])
                    + " and "
                    + selected_currencies[-1]
                )
                template = random.choice(currency_templates)
                policy_sentences.append(
                    template.format(
                        company=company_name,
                        currency_code=currency_code,
                        major_currency=major_currency,
                        money_unit=money_units,
                        end_day=random.randint(28, 31),
                        month=random.choice(months),
                        currencies=currency_list,
                    )
                )

            # Counterparty risk (0-1)
            if random.random() < 0.3:
                template = random.choice(counterparty_templates)
                policy_sentences.append(template.format(company=company_name))

            # No trading policy (0-1)
            if random.random() < 0.4:
                tempate = random.choice(no_trading_templates)
                policy_sentences.append(
                    template.format(
                        company=company_name,
                        currency_code=currency_code,
                        major_currency=major_currency,
                        money_unit=money_units,
                        end_day=random.randint(28, 31),
                        notional1=round(random.uniform(200, 550), 0),
                        notional2=round(random.uniform(200, 550), 0),
                        instrument_list=random.choice(instrument_lists),
                        position_type=random.choice(position_types),
                        metric=random.choice(metrics),
                        year=current_year,
                        hedge_type=random.choice(hedge_types),
                        standard=random.choice(standards),
                        verb=random.choice(impact_verbs),
                        method=random.choice(methods),
                        frequency=random.choice(frequencies),
                        currencies=random.choice(major_currencies),
                        swap_type=random.choice(swap_types),
                        quarter=random.choice(quarters),
                        month=random.choice(months),
                        prev_year=random.choice(past_years),
                        notional_currency=random.choice(currency_codes),
                        notional_amount=round(random.uniform(100, 400), 0),
                        notional=round(random.uniform(100, 400), 0),
                        expiry_year=random.choice(past_years),
                        currency_pair=random.choice(currency_pairs),
                        hedged_item=random.choice(hedged_items),
                        settlement=round(random.uniform(50, 200), 0),
                        amount=round(random.uniform(2, 50), 1),
                        oci_amount=round(random.uniform(0.05, 0.15)),
                        oci_action=random.choice(oci_actions),
                    )
                )

            all_sentences.extend(policy_sentences)

        label = 0 if has_active_derivative else 1

    # Shuffle and select
    random.shuffle(all_sentences)
    selected_sentences = all_sentences[:max_len]
    selected_sentences = [s[0].upper() + s[1:] if s else "" for s in all_sentences]
    # Create paragraph
    paragraph = (
        f"<reportingYear>{reporting_year}</reportingYear> "
        + ". ".join(selected_sentences)
        + "."
    )
    paragraph = re.sub("We's", "Our", paragraph)
    if paragraph.find("{") != -1 or paragraph.find("}") != -1:
        print("Error in format", paragraph)
    return paragraph, label
