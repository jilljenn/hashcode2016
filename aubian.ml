module IntFloat =
struct
    type t = int * float
    let compare = compare
end

module IFMap = Map.Make(IntFloat)

open Scanf

let cmp = ref 0

let debug () = (Printf.printf "%d\n" !cmp; incr cmp)

let dist (a,b) (c,d) =
    let x = abs (a-c) and y = abs (b-d) in
        x * x + y * y
        |> float
        |> sqrt
        |> ceil
        |> int_of_float

let parse () =
    let ic = open_in "mother_of_all_warehouses.in" in
    fscanf ic "%d %d %d %d %d %d" @@ fun nb_r nb_col nb_d deadline max_l p ->
        let weights = Array.init p (fun _ -> fscanf ic " %d" (fun i -> i)) in
        let warehouses = Array.init (fscanf ic " %d" (fun i -> i)) (fun _ ->
            let coord = fscanf ic " %d %d" (fun x y -> (x,y)) in
                coord,Array.init p (fun _ -> fscanf ic " %d" (fun i -> i))) in
        let custom_orders = Array.init (fscanf ic " %d" (fun i -> i)) (fun _ ->
            let coord = fscanf ic " %d %d" (fun x y -> (x,y)) in
            let tab = Array.make p 0 in
                for i = 1 to fscanf ic " %d" (fun j -> j) do
                    fscanf ic " %d" (fun typ -> tab.(typ) <- tab.(typ) + 1);
                done;
            coord,tab
            ) in
            nb_r, nb_col, nb_d, deadline, max_l, p, weights, warehouses, custom_orders;;

let min_non_null tab =
    let a = ref (-1) in
        Array.iteri (fun i x -> if x <> 0 then a := i) tab;
        !a


let write_out l =
    let oc = open_out "output" in
        Printf.fprintf oc "%d" (List.length l);
        List.iter (fun (a,b,c,d,e) -> Printf.fprintf oc "\n%d %c %d %d %d" a b c d e) (List.rev l);
        flush oc

let dist_min weights commands =
    let a = ref 0 in
        Array.iteri (fun i x -> a := !a + x * (commands.(i))) weights;
        !a

let my_alg () =
    let (nb_r, nb_col, nb_d, deadline, max_l, p, weights, warehouses, custom_orders) = parse () in
    let time = ref 0 in
    let prior_drone = ref (IFMap.empty) in
    let prior_tasks = ref (IFMap.empty) in
    let l = ref [] in
        for i = 0 to nb_d-1 do
            prior_drone := IFMap.add (0,Random.float 1.) (i,fst (warehouses.(0))) !prior_drone;
        done;
        for i = 0 to Array.length custom_orders - 1 do
            prior_tasks := IFMap.add (dist_min weights (snd (custom_orders.(i))),Random.float 1.) i !prior_tasks;
        done;
        while !time < deadline && (not (IFMap.is_empty !prior_tasks)) do
            let (((min_tim,_) as swag),(i_drone,pos)) = IFMap.min_binding !prior_drone in
            let (key_task,i_task) = IFMap.min_binding !prior_tasks in
                time := min_tim;
                    match min_non_null (snd (custom_orders.(i_task))) with
                        | -1 -> prior_tasks := IFMap.remove key_task !prior_tasks
                        |  a -> begin
                                    let min_dist = ref max_int and b = ref (-1) in
                                        Array.iteri (fun j (coord,tab) ->
                                            let c = dist coord pos + dist coord (fst (custom_orders.(i_task))) in
                                            if c < !min_dist && tab.(a) <> 0
                                                then (min_dist := c; b := j)
                                                    ) warehouses;
                                        if !b = -1
                                           then prior_tasks := IFMap.remove key_task !prior_tasks
                                           else (
                                                let w_rem = ref max_l in
                                                let l' = ref [] in
                                                let cmpt = ref 0 in
                                                    for z = 0 to p-1 do
                                                        if (weights.(z) <= !w_rem) && ((snd (warehouses.(!b))).(z) > 0) && ((snd (custom_orders.(i_task))).(z) > 0)
                                                            then let to_take = min (min (!w_rem / (weights.(z))) (snd (warehouses.(!b))).(z)) ((snd (custom_orders.(i_task))).(z)) in
                                                                   (incr cmpt; l' := (z,to_take):: !l'; w_rem := !w_rem - (to_take * weights.(z));
                                                let tab = snd (custom_orders.(i_task)) in
                                                    tab.(z) <- tab.(z) - to_take;
                                                let tab' = snd (warehouses.(!b)) in
                                                    tab'.(z) <- tab'.(z) - to_take)
                                                    done;
                                                    prior_drone := IFMap.add (min_tim + !min_dist + (2 * !cmpt),Random.float 1.) (i_drone,fst (custom_orders.(i_task))) (IFMap.remove swag !prior_drone);
                                                    l := (List.map (fun (z,to_take) -> (i_drone,'D',i_task,z,to_take)) !l') @ (List.map (fun (z,to_take) -> (i_drone,'L',!b,z,to_take)) !l') @ !l;
                                                    
(*                                                prior_drone := IFMap.add (min_tim + !min_dist + 2,Random.float 1.) (i_drone,fst (custom_orders.(i_task))) (IFMap.remove swag !prior_drone)
                                                l := (i_drone,'L',!b,a,1)::!l;
                                                l := (i_drone,'D',i_task,a,1)::!l;
                                                let tab = snd (custom_orders.(i_task)) in
                                                    tab.(a) <- tab.(a) - 1;
                                                let tab' = snd (warehouses.(!b)) in
                                                    tab'.(a) <- tab'.(a) - 1 *)
                                                 );
                                end
        done;
        write_out !l;;

my_alg ()
