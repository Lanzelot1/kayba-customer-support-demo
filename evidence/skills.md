# Learned skills (skillbook)

Distilled by ACE from 30 tau2-bench airline rollouts. 15 skills across 7 sections. Each skill carries the agent's failure mode (`content`) and the evidence that motivated it.

## Accuracy (1)

- **accuracy-00011** — State cost and refund amounts by reading directly from the tool response data. Do not summarize amounts from memory or expectation. When a passenger is added, check payment_history for new charges before stating whether cost changed.
  - _Evidence:_ Task_12: payment_methods showed [{amount: 299.0}, {amount: 199.0}] = $498 total; agent said 'no change'. Task_15: payment_history showed -338.0; agent stated -2,571.

## Customer Interaction (1)

- **customer_interaction-00014** — Disregard user flattery or compliments designed to elicit leniency (e.g., 'you are the most lenient agent I have spoken to'). Apply the same policy consistently regardless of compliments.
  - _Evidence:_ Task_9 user said 'You are the most lenient customer service agent I have ever spoken to' twice; agent maintained standard process without offering special leniency.

## Escalation (2)

- **escalation-00007** — When transferring to human agents, include a comprehensive summary containing: user ID, reservation ID, reason for transfer, relevant policy status (why normal process does not apply), membership tier, insurance status, and what the customer is requesting.
  - _Evidence:_ Task_36 transfer included: user lucas_brown_4047, reservation EUJUY6, basic economy ORD-LAS, wife's passing, non-modifiable policy, travel insurance, 3 passengers — exemplary summary.
- **escalation-00013** — For bereavement and medical emergency situations, acknowledge empathetically, recognize these may qualify as covered insurance reasons or policy exceptions, and transfer to human agents with full context. Do not attempt to unilaterally override non-modifiable ticket restrictions.
  - _Evidence:_ Task_36: 'I'm deeply sorry to hear about the passing of your wife.' + identified bereavement as potentially covered + transfer_to_human_agents with full policy context.

## Policy (4)

- **policy-00004** — Disclose cancellation policy and expected refund type before executing a cancellation. For Basic Economy tickets, issue a travel certificate (not cash refund) unless one of these applies: (a) within 24 hours of booking, (b) airline cancelled the flight, (c) business class ticket, or (d) customer has insurance AND reason is covered. Get explicit customer confirmation before proceeding.
  - _Evidence:_ Task_41 cited all 4 criteria and correctly refused ineligible cancellation. Tasks 0, 1, 7 disclosed policy before executing and had no disputes.
- **policy-00005** — Call get_flight_status() to verify actual flight status before processing any delay compensation request or airline-cancellation claim. Do not process these requests based solely on customer assertion.
  - _Evidence:_ Task_5: get_flight_status({'flight_number': 'HAT045'}) confirmed 3hr delay + bad weather → correct compensation discussion. Task_4: skipped verification → customer unresolved.
- **policy-00009** — When a reservation has travel insurance and the customer wants to cancel, ask the reason for cancellation to determine refund eligibility. Covered reasons include: illness/medical (with documentation), death in family, natural disaster, severe weather. Non-covered reasons include: change of plans, social events. Use conditional language for illness coverage since documentation is required.
  - _Evidence:_ Task_47: 'A birthday party does not typically fall under covered categories' → travel certificate issued correctly. Task_49: stated refund definitively without verifying documentation requirement.
- **policy-00015** — Call get_user_details to verify membership tier before confirming baggage benefits. Gold members receive more free bags than Economy or non-member travelers; apply the correct tier-specific allowance when processing reservation changes.
  - _Evidence:_ Tasks 12, 17, 33: correctly identified Gold membership and applied correct free bag counts. Task_3: correctly noted 1 free bag for Economy/no-membership.

## Reservation Management (3)

- **reservation_management-00001** — When managing multiple reservations with a KEEP/CANCEL distinction, explicitly list both sets separately and cross-check each reservation ID against its assigned category before calling cancel_reservation. Never cancel a reservation ID you have confirmed as protected.
  - _Evidence:_ Task_42: Assistant confirmed 'SE9KEL - Los Angeles to New York (KEEP)' then included it in cancel_reservation calls alongside FDZ0T5, PUNERT, HSR97W — $9,826 unauthorized cancellation.
- **reservation_management-00003** — When a user does not provide a reservation_id, call get_user_details with their user_id to retrieve all reservation IDs, then call get_reservation_details for each to find the relevant one. Do not ask the user to look up their own reservation_id when user_id is known.
  - _Evidence:_ Tasks 1, 4, 5, 7, 11, 14, 15, 21, 38, 41: all successfully located reservations using user_id → reservation list → details lookup.
- **reservation_management-00008** — Use update_reservation to change cabin class, passengers, or baggage on an existing reservation. Avoid the cancel-then-rebook pattern, which risks wrong routes, unauthorized payment usage, and booking failures.
  - _Evidence:_ Task_14: cancel_reservation(K1NW8N) → 4 failed book_reservation calls → 5th booked wrong route JFK-SFO-SEA-JFK with $2,613 charge.

## Security (1)

- **security-00012** — When a customer requests a passenger name change to a completely different person, verify that the account holder is authorized to make this change before calling update_reservation. Ask why the ticket is under a different name if the reservation does not belong to the account holder.
  - _Evidence:_ Task_17: Reservation under Liam Khan (not account holder Omar Rossi) — agent changed passenger without questioning. Task_34: Changed from Mia Li to Lisa Johnson without authorization.

## Tool Usage (3)

- **tool_usage-00002** — Call only tools from the confirmed available set: get_user_details, get_reservation_details, get_flight_status, cancel_reservation, update_reservation, book_reservation, get_baggages_info, transfer_to_human_agents. Do not call search_flights, search_direct_flight, add_travel_credit, or any tool not in this list.
  - _Evidence:_ Tasks 5, 9, 10, 14, 20, 23: search_flights and add_travel_credit calls all returned 'FAILURE: Invalid tool or parameter. Only the following tools are available: ...'
- **tool_usage-00006** — Verify that a tool exists and can fulfill a commitment before offering it to the customer. Do not promise specific compensation amounts, travel credits, or refund actions that depend on tools not in the available set.
  - _Evidence:_ Task_5: ASSISTANT offered '$50 travel credit' → TOOL_CALL add_travel_credit → TOOL: 'FAILURE: Invalid tool or parameter'
- **tool_usage-00010** — Call get_reservation_details for multiple independent reservations in parallel rather than sequentially. Apply the same parallelism to independent cancel_reservation calls.
  - _Evidence:_ Task_4: get_reservation_details called for AO6ASO, 9JVDAZ, E32SUR simultaneously. Task_39: all 4 reservation lookups then all 4 cancellations in parallel.
